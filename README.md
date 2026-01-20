# AI Design — University of Trento

This repository hosts materials and code for the AI Design course at the University of Trento. It is intended for enrolled students and contains everything needed to follow along: slides, labs, assignments, project templates, and supporting code.

> Note: Some details are placeholders and will be completed once confirmed (course code, semester, syllabus link, and instructor contacts).

## Course Info

- Course: AI Design (official title/code: TBD)
- University: University of Trento — Department/School: TBD
- Semester/Year: TBD
- Primary language: English
- Instructors: TBD (name, email)
- Syllabus: TBD (link)

## Scope and Audience

- Audience: Students taking AI Design at UniTN
- Contents: lectures, labs, assignments, starter code, projects, readings/resources
- Contributions: PRs from students are welcome (see Contributing)

## Quick Start

Prerequisites

- Python 3.12+ (see `pyproject.toml`)
- uv (fast Python package/dependency manager by Astral)

Install uv (one-time):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# restart your shell to add uv to PATH if needed
```

Set up the environment and run a quick check:

```bash
# Create/refresh a virtualenv and install project deps
uv sync

# Run the sample entry point
uv run python main.py
```

## API Keys Setup

This course uses OpenAI and OpenRouter APIs. Set up your keys once:

```bash
# Copy the template
cp .env.example .env

# Edit .env and add your keys
# OPENAI_API_KEY=sk-...
# OPENROUTER_API_KEY=sk-or-...
```

The `.env` file is git-ignored and will not be committed. All lab scripts automatically load keys from this file.

Get your keys:
- OpenAI: https://platform.openai.com/api-keys
- OpenRouter: https://openrouter.ai/keys

## Repository Structure (planned)

```
lectures/       # Slides and lecture notes
labs/           # Hands-on exercises and notebooks
assignments/    # Homework specs and starter kits
projects/       # Course project templates/guides
resources/      # Readings, datasets pointers, references
scripts/        # Utility scripts (setup, validation, etc.)
```

This structure will be populated incrementally as materials are released.

## Contributing

- Students may open issues and submit PRs for fixes and improvements.
- Keep PRs focused and include a brief description and testing notes.
- For larger changes (e.g., new examples), open an issue first to discuss.
- Code of Conduct: TBD (we can adopt Contributor Covenant if desired).
  
By submitting a contribution, you agree to license your contribution under CC BY-NC-SA 4.0.

## License

All contents of this repository (code and course materials) are licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).

- Attribution required.
- Noncommercial use only.
- Share-alike: derivatives must use CC BY-NC-SA 4.0 (or a compatible license).

See `LICENSE` for the full legal text.

## Logistics (links TBD)

- Course website/LMS (Moodle/other): TBD
- Communication channel (Slack/Teams): TBD
- Submission workflow: TBD (e.g., via LMS; selected tasks via PRs)

## Maintainers

- Instructor(s): TBD
- Teaching Assistants: TBD

---

Questions or changes? Open an issue or PR.
