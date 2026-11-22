"""A tiny local dashboard to view your TraceLite data in a browser.

Run it (from the project folder):

    python -m tracelite.dashboard

Then open:  http://localhost:8765

It uses only Python's standard library -- no installs, same as the rest of the
project. The page auto-refreshes every 3 seconds, so you can run
`examples/real_ollama.py` in another window and watch rows appear live.
"""

import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = os.environ.get("TRACELITE_DB", "traces.db")
PORT = int(os.environ.get("TRACELITE_PORT", "8765"))

PAGE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>TraceLite dashboard</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; background:#0f1115; color:#e6e6e6; }
    h1 { font-size: 1.4rem; margin-bottom: .25rem; }
    .muted { color:#9aa4b2; }
    table { border-collapse: collapse; width: 100%; margin-top: 1.25rem; }
    th, td { padding: 8px 12px; border-bottom: 1px solid #2a2f3a; text-align: left; font-size: 14px; }
    th { color:#9aa4b2; font-weight: 600; }
    .err { color: #ff6b6b; }
    .ok { color: #51cf66; }
    .row:hover { background:#161a22; }
  </style>
</head>
<body>
  <h1>TraceLite dashboard</h1>
  <div id="summary" class="muted">loading...</div>
  <table>
    <thead>
      <tr><th>Time</th><th>Model</th><th>Latency (ms)</th><th>Cost ($)</th><th>Status</th></tr>
    </thead>
    <tbody id="rows"></tbody>
  </table>
  <script>
    async function load() {
      const res = await fetch('/api/traces');
      const data = await res.json();
      const rows = document.getElementById('rows');
      rows.innerHTML = '';
      for (const t of data.traces) {
        const tr = document.createElement('tr');
        tr.className = 'row';
        tr.innerHTML =
          '<td>' + t.ts + '</td>' +
          '<td>' + t.model + '</td>' +
          '<td>' + Number(t.latency_ms || 0).toFixed(1) + '</td>' +
          '<td>' + Number(t.cost_usd || 0).toFixed(6) + '</td>' +
          '<td class="' + (t.status === 'ok' ? 'ok' : 'err') + '">' + t.status + '</td>';
        rows.appendChild(tr);
      }
      document.getElementById('summary').textContent =
        data.count + ' calls  \u00b7  total cost $' + Number(data.total_cost).toFixed(6);
    }
    load();
    setInterval(load, 3000);
  </script>
</body>
</html>"""


def collect_traces(limit=200):
    """Read the most recent traces from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT ts, model, latency_ms, cost_usd, status "
        "FROM traces ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    traces = [dict(r) for r in rows]
    return {
        "count": len(traces),
        "total_cost": sum((t.get("cost_usd") or 0.0) for t in traces),
        "traces": traces,
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/traces":
            body = json.dumps(collect_traces()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        elif self.path == "/":
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            body = b"Not found"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # keep the console quiet


def main():
    print(f"TraceLite dashboard running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.  (Database:", os.path.abspath(DB_PATH) + ")")
    HTTPServer(("localhost", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
