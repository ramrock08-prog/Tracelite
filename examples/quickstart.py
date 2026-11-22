"""Runnable TraceLite demo -- no API keys, no internet, no installs.

It uses a fake "model" so you can see the whole tracking loop work today.
In Week 3 you'll swap `fake_model()` for a real one (Ollama or a free tier).
"""

import os
import sys
import time
import random

# Make `import tracelite` work when running this file directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tracelite as tl  # noqa: E402


def fake_model(prompt):
    """Pretend to be an LLM. Returns (reply, prompt_tokens, completion_tokens)."""
    time.sleep(random.uniform(0.05, 0.4))  # fake "thinking" latency
    reply = f"[fake reply to: {prompt[:40]}...]"
    prompt_tokens = len(prompt.split())
    completion_tokens = random.randint(5, 40)
    return reply, prompt_tokens, completion_tokens


PROMPTS = [
    "Summarise this customer ticket in one line.",
    "Draft a friendly reply to a refund request.",
    "Explain our pricing in two sentences.",
    "Classify this lead as hot or cold.",
]


def main():
    db = tl.init("traces.db")
    print(f"Logging traces to: {os.path.abspath(db)}\n")

    for prompt in PROMPTS:
        with tl.track("gpt-4o-mini", provider="ollama", prompt=prompt) as span:
            reply, pt, ct = fake_model(prompt)
            span.set_response(reply, pt, ct)
        print(f"  logged: {prompt[:45]}")

    # Show that failures get captured too (this one raises on purpose).
    try:
        with tl.track("gpt-4o-mini", provider="ollama", prompt="this one breaks"):
            raise ValueError("model returned 500")
    except ValueError:
        print("  logged: a failure (on purpose)")

    print()
    tl.report()


if __name__ == "__main__":
    main()
