# TraceLite

A tiny, local, **zero-dependency** LLM observability tracker.

Wrap any LLM call, and TraceLite records what happened: the prompt, the
response, how long it took, how many tokens it used, what it cost, and whether
it errored. Then it prints a report.

## Why this exists (the problem)

Every startup ships AI features now. Almost none of them can answer:

- How much are our AI calls costing us this week?
- Is it getting slower?
- How often does it fail?
- Did that prompt change make things worse?

Tools that solve this (LangSmith, Braintrust, Langfuse) are either expensive,
heavy, or too enterprise-shaped for a small team. TraceLite is the smallest
possible version: one file of Python, one SQLite file, one report.

## What's built so far (v0)

- `tl.init("traces.db")` — create/point at the trace database
- `tl.track(model=..., provider=..., prompt=...)` — a context manager that times
  and logs one LLM call (including errors and estimated cost)
- `tl.report()` — prints total calls, cost, latency p50/p95, and error rate,
  **plus** a per-model breakdown, the slowest calls, and cost by day
- Works with **no API keys** — the example uses a fake model, and you can later
  swap in Ollama (free, local) or any free model tier

## Skills you'll actually learn

This is not one skill in isolation. By the end it covers most of what an intern
gets asked about, and each skill is attached to a real piece of the tool:

| Skill | Where you practise it |
| --- | --- |
| Python: functions, classes, context managers, error handling | `tracelite/tracker.py` |
| Databases & SQL | the SQLite schema + the `report()` queries |
| CLI tools & argument parsing | `python -m tracelite report` (Week 2) |
| HTTP & calling APIs | Week 3, wiring a real model (Ollama / free tier) |
| Backend web (FastAPI) | Week 3 dashboard |
| Basic frontend (HTML/JS) | Week 3 dashboard page |
| Writing tests | `tests/test_tracker.py` |
| Git & GitHub | from day one, every change committed |
| Packaging & deployment | Week 4, `pip install -e .` + deploy the dashboard free |

Honest limits: it does **not** teach React, auth, or large-scale system design.
That's OK for a first project. Finishing one real thing beats starting five.

## Run it right now

Requires Python 3.9+. Nothing to install.

```bash
cd tracelite
python examples/quickstart.py
```

You should see a few traces get logged, then a report with these sections:

1. **Summary** — calls, total cost, latency p50/p95, error rate
2. **By model** — cost and speed per model
3. **Slowest calls** — the 3 slowest requests
4. **Cost by day** — spend over time

## Run the tests

```bash
python -m unittest discover -s tests -v
```

All 9 tests should pass (`OK`).

## Roadmap

### Week 0 — set yourself up (done)
- [x] `git init` in this folder and push it to a new **public** GitHub repo
- [x] Commit after every working change with a real message ("add per-model report")
- [x] Learn one: `git add .` -> `git commit -m "..."` -> `git push`

### Week 1 — core tracker (done)
- [x] SQLite schema for traces
- [x] `track()` context manager: latency, errors, token counts
- [x] `report()` CLI: count, cost, p50/p95 latency, error rate
- [x] Add a few real price rows as you learn (see `PRICES` in `tracelite/tracker.py`)
- [x] Read `track()` line by line until you can explain it out loud

### Week 2 — make the report useful + start testing (done)
- [x] Per-model breakdown (cost + latency by model)
- [x] Slowest calls listed
- [x] Daily cost trend (group by date)
- [x] Write tests for `estimate_cost` and the report math

### Week 3 — real model + a viewable dashboard
- [ ] Wire it to a real free model: **Ollama** locally, or a Groq/Gemini free tier
- [ ] Tiny local dashboard (FastAPI + one HTML page) to browse traces

### Week 4 — ship + get seen (STRETCH: the killer feature)
- [ ] `diff` command: rerun saved test prompts against two prompt versions,
      show which outputs changed  <-- this is "LLM regression testing"
- [ ] `pip install -e .` with a real console entry point (`tracelite report`)
- [ ] README screenshots + a 2-minute Loom demo
- [ ] Outreach (see below)

## Outreach playbook (India market)

Target dev-tool and AI-first companies: **Postman, Hasura, Freshworks, Zoho,
Sarvam AI, Yellow.ai, Observe.AI, Haptik**.

1. Post the README + Loom on LinkedIn + X with `#buildinpublic`.
2. Cross-post to **r/developersIndia** and **r/IndiaStartups**.
3. Cold-DM 10–15 founders / eng leads:
   > "Hi [name] — I follow [company]. I built a small tool that tracks LLM
   > cost/latency/failures and catches prompt regressions. Here's a 2-min demo.
   > Would love to show you / get feedback."
4. Parallel track: contribute a good-first-issue to **Langfuse** (open-source LLM
   observability). Visible OSS work is a second proof of the same skill.

## Project structure

```
tracelite/
  README.md
  tracelite/
    __init__.py
    tracker.py        # the whole library
  examples/
    quickstart.py     # runnable demo with a fake model
  tests/
    test_tracker.py   # unit tests
```