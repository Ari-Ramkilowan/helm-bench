# UV Setup Guide - Never Deal With Python Hell Again

This guide ensures you can set up this project correctly every time, avoiding the Python/Anaconda PATH conflicts.

## The Problem We Solved

When you have Anaconda installed, it hijacks your Python PATH even in virtual environments. Traditional `python -m venv` and `source .venv/bin/activate` don't work properly because Anaconda's Python gets used instead of the venv Python.

## The uv Solution

uv handles all of this automatically and replaces the need for Makefiles.

## Initial Setup (One-time per project)

```bash
# 1. Create project virtual environment with correct Python version
uv venv --python 3.12

# 2. Install project dependencies 
uv run setup  # This runs: uv pip install -e .[dev] --python .venv/bin/python

# That's it! No manual activation needed.
```

## Daily Development Commands (Makefile Replacement)

Instead of `make test`, `make lint`, etc., use the dev script:

```bash
# Testing
./scripts/dev test           # Run all tests
./scripts/dev test-watch     # Run tests in watch mode

# Code Quality  
./scripts/dev lint           # Check code style
./scripts/dev format         # Format code
./scripts/dev lint-fix       # Fix auto-fixable issues
./scripts/dev check          # Run both lint and tests

# Pre-PR Workflow (replaces make test && make check && make lint)
./scripts/dev pre-pr         # Format + lint + test - everything you need!

# Project Scripts
./scripts/dev benchmark --client example_client --task text_gen_task_1
./scripts/dev collect-votes
./scripts/dev generate-report

# Environment Management
./scripts/dev setup          # Reinstall dependencies
./scripts/dev clean          # Remove .venv (nuclear option)
```

## Why This Works

- **`uv run`** automatically uses the correct Python from `.venv` without shell activation
- **No PATH conflicts** - uv bypasses shell PATH entirely
- **Scripts in pyproject.toml** replace Makefile functionality
- **Consistent across environments** - works the same on any machine

## Troubleshooting

If you ever get weird Python version errors:

```bash
# Nuclear option - start fresh
uv run clean
uv venv --python 3.12
uv run setup
```

## Key Rules to Follow

1. **NEVER use `python` or `pip` directly** - always use `uv run`
2. **NEVER manually activate** the venv - `uv run` handles it
3. **Add new dependencies** with `uv add package_name` (modifies pyproject.toml)
4. **Install existing dependencies** with `uv run setup`

## What We Added to pyproject.toml

```toml
[tool.uv.scripts]
# Development workflow commands
test = "pytest"
lint = "ruff check"
format = "ruff format"
check = ["ruff check", "pytest"]

# Project-specific commands  
benchmark = "python scripts/1_run_benchmark.py"
setup = "uv pip install -e .[dev] --python .venv/bin/python"
```

This replaces traditional Makefiles with a more modern, Python-native approach.