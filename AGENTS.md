# Repository Guidelines

## Project Structure & Module Organization

- `main.py`: tiny entry point used for quick sanity checks.
- `labs/`: hands-on Python scripts and notes, organized by numbered units (e.g., `labs/01_hello_world/`, `labs/02_standalone_agents/`, `labs/03_ai-api/`).
- `docs/`: supporting course documentation.
- Root Markdown files (e.g., `syllabus.md`): course logistics and reading material.

## Build, Test, and Development Commands

This repo uses `uv` (see `pyproject.toml`) for environment management.

- `uv sync`: create/refresh the virtualenv and install dependencies.
- `uv run python main.py`: run the sample entry point.
- `uv run python labs/01_hello_world/hello_world.py`: run a lab script directly.

LLM-related labs require credentials via environment variables (do not commit secrets):

- `export OPENROUTER_API_KEY="..."` (or `OPENAI_API_KEY="..."`)
- Prefer a local `.env` (already git-ignored) for personal setup.

## Coding Style & Naming Conventions

- Python: 4-space indentation, PEP 8–style naming (`snake_case` for files/functions, `PascalCase` for classes).
- Keep lab code runnable as standalone scripts (`uv run python <file.py>`); avoid introducing unnecessary frameworks.
- When adding new labs, follow the existing numbering pattern: `labs/NN_topic_name/`.

## Testing Guidelines

There is no dedicated automated test suite yet. If you add tests, prefer `pytest` with:

- Tests in `tests/`
- Files named `test_*.py`
- Run locally via `uv run pytest`

## Commit & Pull Request Guidelines

Git history is currently minimal, so there is no strict convention yet. Use:

- Short, imperative commit subjects (e.g., `Add lab on tool calling`, `Fix typo in ai_interface.md`).
- Focused PRs with a clear description, rationale, and “how to run” notes (commands and any required env vars).
- For documentation-only PRs, include a brief preview (e.g., screenshot or pasted rendered snippet) when formatting changes.

## Security & Configuration Tips

- Never commit API keys, tokens, or `.env` files.
- If a change introduces new configuration, document it in `README.md` and keep defaults safe (e.g., fail fast when keys are missing).
