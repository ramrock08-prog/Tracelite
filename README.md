# TraceLite

A tiny, local, **zero-dependency** LLM observability tracker.

Wrap any LLM call, and TraceLite records what happened: the prompt, the
response, how long it took, how many tokens it used, what it cost, and whether
it errored. Then it prints a report — or shows it on a small local dashboard.

## Why this exists (the problem)

Every startup ships AI features now. Almost none of them can answer:

- How much are our AI calls costing us this week?
- Is it getting slower?
- How often does it fail?
- Did that prompt change make things worse?

Tools that solve this (LangSmith, Braintrust, Langfuse) are either expensive,
heavy, or too enterprise-shaped for a small team. TraceLite is the smallest
possible version: one file of Python, one SQLite file, one report.

## What's built so far

- `tl.init("traces.db")` — create/point at the trace database
- `tl.track(model=..., provider=..., prompt=...)` — a context manager that times
  and logs one LLM call (including errors and estimated cost)
- `tl.report()` — prints total calls, cost, latency p50/p95, and error rate,
  **plus** a per-model breakdown, the slowest calls, and cost by day
- `tracelite/dashboard.py` — a tiny local web dashboard (browser view of traces)
- A runnable demo with a **fake** model (`examples/quickstart.py`)
- A runnable demo with a **real local** model via Ollama (`examples/real_ollama.py`)
- A one-file Ollama setup script (`setup_ollama.ps1`)
- Works with **no API keys** and **no installs** — everything runs on your machine

## Skills in this project

| Skill | Where you practise it |
| --- | --- |
| Python: functions, classes, context managers, error handling | `tracelite/tracker.py` |
| Databases & SQL | the SQLite schema + the `report()` queries |
| HTTP & calling APIs | `examples/real_ollama.py` (Ollama HTTP API) |
| Building a web server + frontend | `tracelite/dashboard.py` |
| Writing tests | `tests/test_tracker.py` |
| Git & GitHub | from day one, every change committed |
| Packaging & deployment | not done yet |

## Run it right now

Requires Python 3.9+. Nothing to install.

```bash
python examples/quickstart.py
```

You should see a few traces get logged, then a report with these sections:

1. **Summary** — calls, total cost, latency p50/p95, error rate
2. **By model** — cost and speed per model
3. **Slowest calls** — the 3 slowest requests
4. **Cost by day** — spend over time

## Use a real AI model (Ollama)

TraceLite can track a **real local model**, not just the fake one.

1. One-file setup — installs Ollama, stores models on your chosen drive, starts
   the server, and downloads the model:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\setup_ollama.ps1
   ```
2. Track a real model:
   ```bash
   python examples/real_ollama.py
   ```

Local models are **free**, so their cost shows as `$0` — but the latency is real.

## View the dashboard

```bash
python -m tracelite.dashboard
```

Then open **http://localhost:8765** in your browser. The page auto-refreshes
every 3 seconds, so you can run `examples/real_ollama.py` in another window and
watch rows appear live. (Change the port with the `TRACELITE_PORT` env var.)

## Run the tests

```bash
python -m unittest discover -s tests -v
```

All 9 tests should pass (`OK`).

## What's next

- A `diff` command: rerun saved prompts across two prompt versions and show what
  changed (LLM regression testing)
- Make it installable: `pip install -e .` with a `tracelite report` command
- Screenshots and a short demo video

## Project structure

```
tracelite/
  README.md
  setup_ollama.ps1    # one-file Ollama setup (install + models + server + pull)
  tracelite/
    __init__.py
    tracker.py        # the whole library
    dashboard.py      # tiny local web dashboard
  examples/
    quickstart.py     # demo with a fake model
    real_ollama.py    # demo with a real local model
  tests/
    test_tracker.py   # unit tests
```