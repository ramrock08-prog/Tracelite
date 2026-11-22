"""Run TraceLite against a REAL local AI model, using Ollama.

Ollama runs in the background after install. Then run:

    python examples/real_ollama.py

This is the same idea as quickstart.py, but instead of a fake model it calls a
real one (llama3.2) through Ollama's local HTTP API. Nothing leaves your laptop.
"""

import json
import os
import sys
import urllib.error
import urllib.request

# Make `import tracelite` work when running this file directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tracelite as tl  # noqa: E402

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

PROMPTS = [
    "Summarise this customer ticket in one line: 'I want my money back'.",
    "Draft a friendly one-line reply to a refund request.",
    "Explain our pricing in two short sentences.",
]


def ask_ollama(prompt):
    """Call the real model. Returns (reply, prompt_tokens, completion_tokens).

    Ollama reports token counts as `prompt_eval_count` (input) and `eval_count`
    (output), which is exactly what TraceLite needs for its cost/latency report.
    """
    body = json.dumps(
        {"model": MODEL, "prompt": prompt, "stream": False}
    ).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.loads(response.read().decode("utf-8"))
    return (
        data.get("response", ""),
        data.get("prompt_eval_count", 0),
        data.get("eval_count", 0),
    )


def main():
    db = tl.init("traces.db")
    print(f"Logging traces to: {os.path.abspath(db)}")
    print(f"Using a REAL local model: {MODEL} (via Ollama)\n")

    for prompt in PROMPTS:
        try:
            with tl.track(MODEL, provider="ollama", prompt=prompt) as span:
                reply, pt, ct = ask_ollama(prompt)
                span.set_response(reply, pt, ct)
            print(f"  logged: {prompt[:45]} -> {reply[:40].strip()!r}")
        except urllib.error.URLError:
            print("\nCould not reach Ollama. Is it running?")
            print("Open a new terminal and run:  ollama serve")
            return

    print()
    tl.report()


if __name__ == "__main__":
    main()
