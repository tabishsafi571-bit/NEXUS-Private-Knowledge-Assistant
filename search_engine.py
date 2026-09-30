
import re
from collections import Counter


def tokenize(text):
    return re.findall(r"[a-zA-Z0-9_]+|[^\W\d_]+", text.lower())


def search_documents(question, documents, limit=5):
    query_words = set(tokenize(question))

    if not query_words:
        return []

    results = []

    for document in documents:
        text = document["text"]
        words = tokenize(text)
        counts = Counter(words)

        score = sum(
            min(counts[word], 5) for word in query_words
        )

        # Give a small bonus when the complete query appears.
        if question.strip().lower() in text.lower():
            score += 5

        if score <= 0:
            continue

        best_position = 0
        lower_text = text.lower()

        for word in query_words:
            position = lower_text.find(word)
            if position >= 0:
                best_position = position
                break

        start = max(0, best_position - 180)
        end = min(len(text), best_position + 520)
        excerpt = text[start:end].strip()

        if start > 0:
            excerpt = "..." + excerpt
        if end < len(text):
            excerpt += "..."

        results.append({
            "name": document["name"],
            "path": document["path"],
            "excerpt": excerpt,
            "score": score,
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]