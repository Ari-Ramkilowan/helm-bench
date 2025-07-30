# Helm Bench: The Client-Centred LLM Evaluation Platform

This repository contains the code for Helm Bench, a powerful, client-centred platform for evaluating and optimising Large Language Models (LLMs).

---

## Installation

These instructions assume you have Python 3.12 and `uv` installed.

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd helm-bench
    ```

2.  **Create and Activate the Virtual Environment**
    ```bash
    python3.12 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    Install the project and all its development dependencies using `uv`:
    ```bash
    uv pip install -e .[dev]
    ```

### Troubleshooting

**Error: `No solution found when resolving dependencies` due to Python version mismatch.**

If you have multiple Python versions installed (e.g., via Anaconda), `uv` might try to use the wrong one. You can force `uv` to use the correct Python interpreter from your virtual environment by using the `--python` flag.

This is the recommended command if you encounter version conflicts:

```bash
# From the root of the project directory
uv pip install -e .[dev] --python ./.venv/bin/python
```
