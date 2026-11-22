"""Run TraceLite against a REAL local AI model, using Ollama.

Ollama runs in the background after install. Then run:

    python examples/real_ollama.py

This is the same idea as quickstart.py, but instead of a fake model it calls a
real one (llama3.2) through Ollama's local HTTP API. Nothing leaves your laptop.
"""

import os
import sys
import urllib.error

# Make `import tracelite` work when running this file directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tracelite as tl  # noqa: E402
from tracelite import ollama  # noqa: E402

MODEL = "llama3.2"

PROMPTS = [
    "Summarise this customer ticket in one line: 'I want my money back'.",
    "Draft a friendly one-line reply to a refund request.",
    "Explain our pricing in two short sentences.",
]


def main():
    db = tl.init("traces.db")
    print(f"Logging traces to: {os.path.abspath(db)}")
    print(f"Using a REAL local model: {MODEL} (via Ollama)\n")

    for prompt in PROMPTS:
        try:
            with tl.track(MODEL, provider="ollama", prompt=prompt) as span:
                out = ollama.ask(prompt, MODEL)
                span.set_response(
                    out["response"], out["prompt_tokens"], out["completion_tokens"]
                )
            print(f"  logged: {prompt[:45]} -> {out['response'][:40].strip()!r}")
        except urllib.error.URLError:
            print("\nCould not reach Ollama. Is it running?")
            print("Open a new terminal and run:  ollama serve")
            return

    print()
    tl.report()


if __name__ == "__main__":
    main()
