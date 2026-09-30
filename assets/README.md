
# NEXUS — Private Knowledge Assistant

NEXUS is a Python desktop prototype for searching personal notes locally.

## Features
- Reads TXT and Markdown documents.
- Searches user-selected folders.
- Displays matching document content and source paths.
- Includes optional integration with a local Ollama AI service.
- Falls back to document excerpts when local AI is unavailable.

## Current Status
The local document search prototype has been tested.
The basic search uses keyword matching.
Ollama integration requires separate setup and testing.
PDF support, semantic search, and Snapdragon-specific optimization
are not currently implemented.

## Run
Install Python 3, open a terminal in the project directory, and run:

    python main.py
