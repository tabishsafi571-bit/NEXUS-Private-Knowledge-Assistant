
import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen2.5:3b"


def generate_answer(question, results, model=DEFAULT_MODEL):
    if not results:
        return (
            "No matching information was found in your indexed "
            "documents. Try different keywords or add relevant notes."
        ), "Search only"

    context = "\n\n".join(
        f"Source: {item['name']}\n"
        f"Location: {item['path']}\n"
        f"Excerpt: {item['excerpt']}"
        for item in results
    )

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Answer using only the supplied document excerpts. "
                    "If the excerpts do not contain the answer, say so. "
                    "Do not invent facts. Mention the source filename."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {question}\n\nDocuments:\n{context}",
            },
        ],
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))

        answer = data.get("message", {}).get("content", "").strip()
        if answer:
            return answer, f"Local AI: {model}"

    except (OSError, ValueError, KeyError, urllib.error.URLError):
        pass

    fallback = (
        "Local AI is unavailable. Here are the matching excerpts "
        "from your documents:\n\n"
        + "\n\n".join(
            f"[{item['name']}]\n{item['excerpt']}"
            for item in results
        )
    )
    return fallback, "Search only — local AI unavailable"
