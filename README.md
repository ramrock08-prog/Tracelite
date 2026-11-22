# TraceLite

A tiny, local, **zero-dependency** LLM observability tracker.

Wrap any LLM call, and TraceLite records what happened: the prompt, the
response, how long it took, how many tokens it used, what it cost, and whether
it errored. Then it prints a report — or shows it on a small local dashboard.
It can also catch **prompt regressions**: answers that changed after a prompt edit.

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
- `tracelite dashboard` — a tiny local web dashboard (browser view)
- `tracelite diff` — **LLM regression testing** (what changed vs baseline)
- `tracelite/ollama.py` — one small helper that talks to a real local model
- Runnable demos with a **fake** model (`examples/quickstart.py`) and a **real**
  local model (`examples/real_ollama.py`)
- A one-file Ollama setup script (`setup_ollama.ps1`)
- Works with **no API keys** and **no installs** — everything runs on your machine

## Skills in this project

| Skill | Where you practise it |
| --- | --- |
| Python: functions, classes, context managers, error handling | `tracelite/tracker.py` |
| Databases & SQL | the SQLite schema + the `report()` queries |
| HTTP & calling APIs | `tracelite/ollama.py` (Ollama HTTP API) |
| Building a web server + frontend | `tracelite/dashboard.py` |
| LLM regression testing (evals) | `tracelite/diff.py` |
| Writing tests | `tests/test_tracker.py` |
| Packaging (a real CLI) | `pyproject.toml` + `tracelite/cli.py` |
| Git & GitHub | from day one, every change committed |

## Install it (adds the `tracelite` command)

```bash
pip install -e .
```

Now you can run it from anywhere:

```bash
tracelite report          # cost / latency / error report
tracelite dashboard       # local web dashboard
tracelite diff --save     # save an LLM regression baseline
```

## Run it without installing

Requires Python 3.9+. Nothing to install.

```bash
python examples/quickstart.py
```

You should see a few traces get logged, then a report with four sections:
summary, by model, slowest calls, and cost by day.

## Use a real AI model (Ollama)

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
tracelite dashboard
```

Then open **http://localhost:8765** in your browser. The page auto-refreshes
every 3 seconds, so you can run `examples/real_ollama.py` in another window and
watch rows appear live. (Change the port with the `TRACELITE_PORT` env var.)

## Catch prompt regressions (LLM diff)

Save what the model answers today, then rerun the same prompts later and see
exactly which answers changed — so a prompt edit that breaks other cases can't
sneak through.

```bash
tracelite diff --save    # save the baseline (golden.json)
tracelite diff           # rerun and compare
```

It runs at `temperature 0` for repeatability. Edit `testcases.json` to choose
which prompts it tests.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

All 9 tests should pass (`OK`).

## What's next

- Screenshots and a short demo video

## Project structure

```
tracelite/
  README.md
  LICENSE
  pyproject.toml      # packaging: makes the `tracelite` command
  setup_ollama.ps1    # one-file Ollama setup (install + models + server + pull)
  testcases.json      # prompts used by the regression check
  tracelite/
    __init__.py
    tracker.py        # the meter: log calls, print the report
    dashboard.py      # tiny local web dashboard
    diff.py           # LLM regression testing
    ollama.py         # helper to call a real local model
    cli.py            # the `tracelite` command
  examples/
    quickstart.py     # demo with a fake model
    real_ollama.py    # demo with a real local model
  tests/
    test_tracker.py   # unit tests
```