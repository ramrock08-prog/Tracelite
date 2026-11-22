# My Project Plan

## 1. What my project is

**TraceLite** — a small Python tool that watches AI calls and reports how much
they cost, how slow they are, and when they fail.

- It records every AI call (the prompt, the reply, the time it took, the money
  it cost, and any error) into a small database.
- Then it prints a report: total cost, average speed, and error rate.
- Later it gets a simple web page to view all this.

**The real problem it solves:** every startup now uses AI inside its product,
but they cannot see how much that AI costs or when it breaks. TraceLite gives
them that visibility. This is a real, current, expensive pain.

## 2. Which companies I am targeting

India's **developer-tool** and **AI** companies, because they build products for
developers and use AI heavily — so this tool speaks their exact language:

- **Postman** (API tools)
- **Hasura** (developer tools)
- **Freshworks** (business software)
- **Zoho** (business software)
- **Sarvam AI** (AI models)
- **Yellow.ai** (AI chatbots)
- **Observe.AI** (AI for support teams)
- **Haptik** (AI assistants)

I am not applying to one company. I am sending my demo to about **15 people**
at these types of companies (founders, and engineering leads).

## 3. The complete step-by-step

### STEP 0 — Today: see it work (30 min)
- [ ] Run the project once:
      `cd F:\tracelite` then `python examples/quickstart.py`
- [ ] Look at the report it prints. That report is the whole point of the tool.

### STEP 1 — Days 1-2: understand the code
- [ ] Read `tracelite/tracker.py` and learn the story of `track()`:
      set up -> your code runs -> always save.
- [ ] Make a small change and run again (change the `0.4` to `2.0` in
      `examples/quickstart.py` and watch latency grow).
- [ ] Rule to learn by: *change something, break it, read the error, fix it.*

### STEP 2 — Days 3-7 (Week 1): put it on GitHub
- [ ] Install Git (if not installed): https://git-scm.com/downloads
- [ ] Make a free account on https://github.com
- [ ] Create a new **public** repository called `tracelite`
- [ ] In the `F:\tracelite` folder, run these one at a time:
      ```
      git init
      git add .
      git commit -m "first working version"
      git branch -M main
      git remote add origin https://github.com/YOUR-NAME/tracelite.git
      git push -u origin main
      ```
- [ ] Refresh the GitHub page. Your code is now online. This link goes in your
      internship messages.
- [ ] After this, save every change with:
      `git add .` -> `git commit -m "what I changed"` -> `git push`

### STEP 3 — Week 2: make the report useful + add tests
- [ ] Add a **per-model breakdown**: cost and speed for each model separately.
- [ ] List the **slowest calls**.
- [ ] Add a **daily cost** line (group by date).
- [ ] Write 2-3 small tests for `estimate_cost` and the report numbers.
- [ ] Commit and push each time.

### STEP 4 — Week 3: connect a real AI model + a web page
- [ ] Install **Ollama** (free, runs AI on your own laptop, no money, no keys):
      https://ollama.com
- [ ] Replace the fake model in `quickstart.py` with a real Ollama call.
- [ ] Build a tiny local web page (FastAPI + one HTML file) to view the traces.
- [ ] Commit and push.

### STEP 5 — Week 4: package, deploy, and record a demo
- [ ] Add a console command so people can run `tracelite report`.
- [ ] Deploy the web page free (Render or Railway) so it has a live link.
- [ ] Record a **2-minute video** (Loom) showing: the problem -> the tool -> the report.
- [ ] Finish the README with 1-2 screenshots.

### STEP 6 — After Week 4: outreach (the real unlock)
- [ ] Post the repo + video on LinkedIn and X. Tag it `#buildinpublic`.
- [ ] Post it in **r/developersIndia** and **r/IndiaStartups**.
- [ ] Send this message to ~15 people (founders / eng leads) at the companies above:

      > Hi [name] — I follow [company]. I built a small tool that tracks AI
      > cost, speed, and failures, and catches AI prompt regressions.
      > Here's a 2-minute demo: [link]. Would love to show you / get feedback.

- [ ] Repeat weekly with small improvements. Reply to every response.

## 4. Yes, this already exists (and why that's fine)

Existing tools: **Langfuse, LangSmith, Helicone, Braintrust, Arize Phoenix,
LiteLLM, Traceloop/OpenLLMetry**, plus Datadog and W&B Weave.

Why this is good news:
- It **proves the problem is real** -- companies pay for this.
- For a first project, **originality is not the goal.** Everyone learns by
  rebuilding things. Founders know an intern is not inventing something new.
- Companies care about: *do you understand the problem, and can you ship?*
  Your project answers both.

**My twist so I am not just a clone (pick 1-2):**
- Simplicity: one file, no signup, no cloud, runs on the laptop, data stays local.
- The regression `diff` feature (rerun prompts across two versions, show changes).
- India angle: cost in INR, Hindi/multilingual prompts, plain-English report.

**Also useful:** read the open-source ones (Langfuse, LiteLLM) to learn. In
outreach I can honestly say "inspired by Langfuse, focused on simplicity."

## 5. Which roles this project fits

**Apply to these (best fit):**
- **AI Engineer Intern / GenAI / LLMOps Intern** -- you track AI cost,
  latency, failures, and prompt regressions. That IS AI engineering.
- **Backend Engineer Intern (Python)** -- classes, context managers, errors,
  SQLite, SQL. Solid backend basics.
- **Software Engineer Intern (general)** -- a full, shipped, git-tracked project.

Job titles to search in India: "AI Engineer Intern", "GenAI Intern",
"Backend Developer Intern", "SDE Intern".

**One small addition turns it into these:**
- Full-stack -> add the Week-3 web dashboard.
- Data Engineer -> the daily cost trends + SQL grouping.
- Platform/Infra -> deploy it + a Dockerfile.
- DevRel / Developer Tools -> a blog post + demo video.

**Not a fit (don't apply with this):**
- ML Research / Data Scientist (needs model training + math).
- Frontend / Mobile.

**My one-line profile:** a Python backend engineer who understands AI in
production. That is the most in-demand intern profile in India right now.

## 6. The rule for the whole month

Ship early, show it, keep improving. A finished Week-2 version sent to 20 people
beats a perfect Week-4 version nobody sees.
