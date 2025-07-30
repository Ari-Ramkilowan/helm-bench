# Technical Specification: Phase 1 - The Flexible Multi-Task Runner

**Version:** 1.0
**Date:** July 2025
**Status:** Proposed

---

## 1. Overview

This document outlines the technical implementation for Phase 1 of the Helm Evaluation Platform. The goal is to build the core engine capable of running different types of evaluation tasks, organised by client, and saving the results in a structured format. Development will be strictly test-driven.

As per our guidelines, we will establish a `src/helm_bench` directory for core logic, keeping the `scripts/` directory for thin CLI wrappers.

## 2. File & Directory Structure

We will create the following new files and directories:

```
helm-bench/
├── src/
│   └── helm_bench/
│       ├── __init__.py
│       ├── config.py       # Loads model and run configurations.
│       ├── data_models.py  # Pydantic models for tasks, results, etc.
│       ├── llm_clients.py  # Base and mock LLM client implementations.
│       ├── runner.py       # Main orchestration logic.
│       └── tasks.py        # Task dispatcher and handlers.
├── datasets/
│   └── example_client/
│       ├── text_gen_task_1/
│       │   ├── task.json
│       │   └── prompts.jsonl
│       └── image_extract_task_1/
│           ├── images/
│           │   └── sample_image_1.png
│           ├── task.json
│           └── prompts.jsonl
└── tests/
    ├── __init__.py
    ├── test_config.py
    ├── test_data_models.py
    ├── test_llm_clients.py
    ├── test_runner.py
    └── test_tasks.py
```

## 3. Data Models (`src/helm_bench/data_models.py`)

We will use Pydantic for type-safe data modelling.

```python
from pydantic import BaseModel, FilePath
from typing import Literal, List, Dict

class Prompt(BaseModel):
    prompt_id: str
    prompt_text: str

class TextGenerationTask(BaseModel):
    task_id: str
    task_type: Literal["text_generation"]
    client_id: str
    prompts: List[Prompt]

class ImageExtractionTask(BaseModel):
    task_id: str
    task_type: Literal["image_extraction"]
    client_id: str
    prompts: List[Prompt]
    image_path: FilePath

class ModelConfig(BaseModel):
    model_id: str
    provider: str
    # Future fields: api_key, endpoint, etc.

class BenchmarkResult(BaseModel):
    client_id: str
    task_id: str
    prompt_id: str
    model_id: str
    prompt_text: str
    response: str
    # Future fields: cost, latency, etc.
```

## 4. Core Components

- **`config.py`:** Will contain a function `load_models() -> List[ModelConfig]` that reads a (future) configuration file to get the list of models to test against.

- **`llm_clients.py`:**
    - An abstract base class `LLMClient` with methods like `get_text_response(prompt: str) -> str` and `get_vision_response(prompt: str, image_path: FilePath) -> str`.
    - A `FakeLLMClient` that inherits from `LLMClient` and returns deterministic, hardcoded responses for testing purposes. It will be the default client for Phase 1.

- **`tasks.py`:**
    - A `load_task(client_id: str, task_id: str) -> BaseModel` function that reads the `task.json` and `prompts.jsonl` and returns the appropriate Pydantic model (`TextGenerationTask` or `ImageExtractionTask`).
    - A `run_task(task: BaseModel, client: LLMClient, model: ModelConfig) -> List[BenchmarkResult]` function that acts as a dispatcher. It checks the `task_type` and calls the appropriate handler (e.g., `_run_text_generation(...)`).

- **`runner.py`:**
    - The main `run_benchmark(client_id: str, task_id: str)` function.
    - **Workflow:**
        1.  Loads the specified task using `tasks.load_task()`.
        2.  Loads the models to test against using `config.load_models()`.
        3.  Initialises the `FakeLLMClient`.
        4.  Iterates through each model.
        5.  For each model, calls `tasks.run_task()`.
        6.  Collects all `BenchmarkResult` objects.
        7.  Saves the list of results to a timestamped JSON file in `results/`.

## 5. CLI Interface (`scripts/1_run_benchmark.py`)

The script will be a thin wrapper around the `runner.py` module.

- **Usage:** `python scripts/1_run_benchmark.py --client <client_id> --task <task_id>`
- **Libraries:** It will use `argparse` or `typer` for parsing command-line arguments.
- **Logic:** It will parse the args and call `helm_bench.runner.run_benchmark(client_id, task_id)`.

## 6. Testing Strategy (TDD)

We will create the following tests *before* writing the implementation code:

1.  **`test_data_models.py`:** Test that Pydantic models correctly validate and reject data (e.g., a task with a missing `task_type`).
2.  **`test_tasks.py`:**
    - Write a test to ensure `load_task` can correctly load a sample `task.json` and `prompts.jsonl` from a temporary directory.
    - Write a test for the `run_task` dispatcher to ensure it calls the correct (mocked) handler based on `task_type`.
3.  **`test_llm_clients.py`:** Test that the `FakeLLMClient` returns its expected hardcoded responses.
4.  **`test_runner.py`:** Write an integration test for `run_benchmark`. This test will:
    - Create a fake client/task directory structure.
    - Call `run_benchmark()`.
    - Assert that the correct `results.json` file is created and that its content matches the expected output from the `FakeLLMClient`.
