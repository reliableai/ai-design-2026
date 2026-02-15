# Designing Large Scale AI Systems — University of Trento, Spring 2026

Course materials for building AI-powered software systems using LLMs as components.

## Quick Start

### 1. Install uv (one-time)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager. Install it:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal after installing so `uv` is on your PATH.

### 2. Clone and install

```bash
git clone https://github.com/reliableai/ai-design-2026.git
cd ai-design-2026
uv sync
```

This creates a virtual environment and installs all dependencies. You don't need to activate it — `uv run` handles that.

### 3. Set up API keys

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...
```

Get your keys:
- **OpenAI**: https://platform.openai.com/api-keys (required for voice and image labs)
- **OpenRouter**: https://openrouter.ai/keys (cheaper alternative for text-only labs)

The `.env` file is git-ignored and will never be committed.

### 4. Verify it works

```bash
uv run python docs/labs/01_hello_world/1_chat.py
```

You should see an LLM response and a timing line. If so, you're ready.

### macOS note: voice lab

The voice lab (`3_voice.py`) needs PortAudio for microphone access:

```bash
brew install portaudio
```

macOS will also prompt you to grant microphone permission to your terminal on first run.

## Running labs

Each lab is a set of Python scripts you run directly:

```bash
uv run python docs/labs/01_hello_world/1_chat.py       # Chat completion
uv run python docs/labs/01_hello_world/2_streaming.py   # Streaming
uv run python docs/labs/01_hello_world/3_voice.py       # Voice pipeline
uv run python docs/labs/01_hello_world/4_image.py       # Image generation
```

Some labs also have Jupyter notebooks for interactive demos:

```bash
uv run jupyter lab docs/labs/01_hello_world/lesson1_demo.ipynb
```

## Running tests

```bash
uv run pytest tests/ -v -m "not slow"     # Skip expensive tests (image generation)
uv run pytest tests/ -v                    # Run everything
```

## Repository Structure

```
docs/
├── index.html                    # Course website
├── labs/
│   ├── 01_hello_world/           # L1: API calls — chat, streaming, voice, image
│   ├── 02_standalone_agents/     # L2: Stateless → stateful → memory-optimized agents
│   ├── 03_ai-api/                # L3: Tool calling, MCP
│   └── 04_eval/                  # L5: Evaluation and "Optimizing in the Dark"
└── style.css
tests/                            # Test suites for labs
```

## License

CC BY-NC-SA 4.0. See `LICENSE`.
