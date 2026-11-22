"""Talk to a local Ollama model over its HTTP API.

This is the one place that knows how to call Ollama, so the rest of the project
does not repeat the HTTP code.
"""

import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask(prompt, model="llama3.2", temperature=0.0, timeout=180):
    """Send one prompt to Ollama.

    Returns a dict with the reply text and token counts, e.g.:
        {"response": "...", "prompt_tokens": 12, "completion_tokens": 30}

    temperature=0 asks the model to be as repeatable as possible, which makes
    regression testing meaningful.
    """
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    return {
        "response": data.get("response", ""),
        "prompt_tokens": data.get("prompt_eval_count", 0),
        "completion_tokens": data.get("eval_count", 0),
    }
