
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB per file


def load_documents(folder_path):
    """Read supported text documents from a selected folder."""
    root = Path(folder_path).expanduser()

    if not root.exists() or not root.is_dir():
        raise ValueError("Please select a valid folder.")

    documents = []
    skipped = 0

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Skip hidden files and files inside hidden directories.
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue

        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                skipped += 1
                continue

            text = path.read_text(encoding="utf-8", errors="replace").strip()
            if text:
                documents.append({
                    "name": path.name,
                    "path": str(path.resolve()),
                    "text": text,
                })
        except (OSError, PermissionError):
            skipped += 1

    return documents, skipped