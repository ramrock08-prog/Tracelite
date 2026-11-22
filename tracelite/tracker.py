"""Core of TraceLite: log LLM calls to SQLite, then report on them.

Standard library only, on purpose. No installs, no API keys required to start.
"""

import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime, timezone

# Where traces are stored. Override by calling init("some/other.db").
_DB_PATH = "traces.db"

# Rough price in USD per 1,000,000 tokens: (input, output).
# These change often -- update them as you learn. Local models are free.
PRICES = {
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "claude-3-5-sonnet": (3.00, 15.00),
    "llama3": (0.0, 0.0),  # running locally via Ollama = no cost
}


def init(path="traces.db"):
    """Create the trace database / point TraceLite at it."""
    global _DB_PATH
    _DB_PATH = path
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS traces (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                ts                TEXT    NOT NULL,
                model             TEXT,
                provider          TEXT,
                prompt            TEXT,
                response          TEXT,
                latency_ms        REAL,
                prompt_tokens     INTEGER,
                completion_tokens INTEGER,
                cost_usd          REAL,
                status            TEXT,
                error             TEXT
            )
            """
        )
    return _DB_PATH


def _connect():
    return sqlite3.connect(_DB_PATH)


def estimate_cost(model, prompt_tokens=0, completion_tokens=0):
    """Estimate USD cost for a call, using the PRICES table."""
    price_in, price_out = PRICES.get(model, (0.0, 0.0))
    return (prompt_tokens / 1_000_000) * price_in + (
        completion_tokens / 1_000_000
    ) * price_out


class _Span:
    """Collects the details of one call while it runs."""

    def __init__(self, model, provider, prompt):
        self.model = model
        self.provider = provider
        self.prompt = prompt
        self.response = None
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.started_at = 0.0

    def set_response(self, text, prompt_tokens=0, completion_tokens=0):
        """Call this inside the `with` block once you have the model's reply."""
        self.response = text
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


@contextmanager
def track(model, provider="unknown", prompt=""):
    """Time and log one LLM call.

    Usage:
        with tl.track("llama3", provider="ollama", prompt=my_prompt) as span:
            reply, pt, ct = call_the_model(my_prompt)
            span.set_response(reply, pt, ct)
    """
    span = _Span(model, provider, prompt)
    span.started_at = time.perf_counter()
    status = "ok"
    error = None
    try:
        yield span
    except Exception as exc:  # record the failure, then let it bubble up
        status = "error"
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        latency_ms = (time.perf_counter() - span.started_at) * 1000
        cost = estimate_cost(span.model, span.prompt_tokens, span.completion_tokens)
        with _connect() as conn:
            conn.execute(
                """
                INSERT INTO traces
                    (ts, model, provider, prompt, response, latency_ms,
                     prompt_tokens, completion_tokens, cost_usd, status, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    span.model,
                    span.provider,
                    span.prompt,
                    span.response,
                    latency_ms,
                    span.prompt_tokens,
                    span.completion_tokens,
                    cost,
                    status,
                    error,
                ),
            )


def _percentile(sorted_values, pct):
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (pct / 100) * (len(sorted_values) - 1)
    low = int(rank)
    high = min(low + 1, len(sorted_values) - 1)
    frac = rank - low
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * frac


def report():
    """Print a summary of everything logged so far."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT latency_ms, cost_usd, status FROM traces"
        ).fetchall()

    if not rows:
        print("No traces yet -- run examples/quickstart.py first.")
        return

    latencies = sorted(r[0] for r in rows)
    total_cost = sum(r[1] or 0.0 for r in rows)
    errors = sum(1 for r in rows if r[2] != "ok")

    print("TraceLite report")
    print("-" * 34)
    print(f"calls        : {len(rows)}")
    print(f"total cost   : ${total_cost:.6f}")
    print(f"avg cost/call: ${total_cost / len(rows):.6f}")
    print(f"latency p50  : {_percentile(latencies, 50):.1f} ms")
    print(f"latency p95  : {_percentile(latencies, 95):.1f} ms")
    print(f"errors       : {errors} ({errors / len(rows) * 100:.1f}%)")

    # Week 2: per-model breakdown
    with _connect() as conn:
        by_model = conn.execute(
            """
            SELECT model, COUNT(*), SUM(cost_usd), AVG(latency_ms)
            FROM traces
            GROUP BY model
            ORDER BY SUM(cost_usd) DESC
            """
        ).fetchall()

    print()
    print("By model")
    print("-" * 34)
    for model, count, cost, avg_latency in by_model:
        print(
            f"{model:<14} {count:>3} calls  "
            f"{avg_latency:>7.1f} ms avg  ${(cost or 0.0):.6f}"
        )
