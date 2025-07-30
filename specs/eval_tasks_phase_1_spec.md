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
│       ├── config.py         # Loads model and run configurations.
│       ├── data_models.py    # Pydantic models for tasks, results, etc.
│       ├── data_manager.py   # Data loading, validation, and preparation.
│       ├── privacy.py        # Privacy controls and data sensitivity handling.
│       ├── synthetic.py      # Synthetic data generation tools.
│       ├── templates.py      # Template-based evaluation dataset creation.
│       ├── llm_clients.py    # Base and mock LLM client implementations.
│       ├── runner.py         # Main orchestration logic.
│       └── tasks.py          # Task dispatcher and handlers.
├── datasets/
│   ├── example_client/
│   │   ├── text_gen_task_1/
│   │   │   ├── task.json
│   │   │   ├── prompts.jsonl
│   │   │   └── data/
│   │   │       ├── inputs.jsonl
│   │   │       ├── expected.jsonl
│   │   │       ├── metadata.json
│   │   │       └── schema.json
│   │   └── image_info_extract_task_1/
│   │       ├── task.json
│   │       ├── prompts.jsonl
│   │       ├── data/
│   │       │   ├── inputs.jsonl
│   │       │   ├── metadata.json
│   │       │   └── schema.json
│   │       └── images/
│   │           └── sample_image_1.png
│   ├── templates/
│   │   ├── contract_analysis/
│   │   ├── email_summarization/
│   │   ├── document_qa/
│   │   └── customer_support/
│   └── generators/
│       ├── business_emails.py
│       ├── legal_contracts.py
│       └── customer_reviews.py
└── tests/
    ├── __init__.py
    ├── test_config.py
    ├── test_data_models.py
    ├── test_data_manager.py
    ├── test_privacy.py
    ├── test_synthetic.py
    ├── test_templates.py
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

class ImageInformationExtractionTask(BaseModel):
    task_id: str
    task_type: Literal["image_information_extraction"]
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
    input_data: dict          # The input data used for this evaluation
    data_source_type: str     # "client_provided", "synthetic", "template", "public"
    # Future fields: cost, latency, etc.

class DataSource(BaseModel):
    type: Literal["client_provided", "synthetic", "template", "public"]
    privacy_level: Literal["confidential", "internal", "public"]
    format: str
    count: int
    schema_file: Optional[str] = None

class EvaluationData(BaseModel):
    input_text: str
    expected_output: Optional[str] = None
    metadata: dict = {}
    
class ImageEvaluationData(BaseModel):
    image_path: FilePath
    input_prompt: str
    expected_output: Optional[str] = None
    metadata: dict = {}
```

## 4. Core Components

- **`config.py`:** Will contain a function `load_models() -> List[ModelConfig]` that reads a (future) configuration file to get the list of models to test against.

- **`data_manager.py`:** Central data handling component:
    - `load_evaluation_data(client_id: str, task_id: str) -> List[EvaluationData]` - Load and validate input data
    - `validate_data_schema(data: List[dict], schema_file: str) -> bool` - Ensure data meets requirements
    - `prepare_data_for_evaluation(task: BaseModel) -> List[EvaluationData]` - Prepare data for model evaluation

- **`privacy.py`:** Data sensitivity and privacy controls:
    - `check_privacy_level(data_source: DataSource) -> bool` - Validate privacy requirements
    - `sanitize_results(results: List[BenchmarkResult], privacy_level: str) -> List[BenchmarkResult]` - Remove sensitive info from outputs
    - `log_data_access(client_id: str, task_id: str, user: str)` - Audit trail for data access

- **`synthetic.py`:** Synthetic data generation:
    - `generate_business_emails(count: int) -> List[EvaluationData]` - Create fake business email scenarios
    - `generate_legal_contracts(count: int) -> List[EvaluationData]` - Create fake contract analysis data
    - `generate_customer_reviews(count: int) -> List[EvaluationData]` - Create fake customer feedback data

- **`templates.py`:** Template-based evaluation creation:
    - `load_template(template_name: str) -> TaskTemplate` - Load pre-built evaluation templates
    - `create_task_from_template(template: TaskTemplate, client_id: str, customizations: dict) -> BaseModel` - Generate client-specific tasks from templates

- **`llm_clients.py`:**
    - An abstract base class `LLMClient` with methods like `get_text_response(prompt: str, input_data: str) -> str` and `get_vision_response(prompt: str, image_path: FilePath) -> str`.
    - A `FakeLLMClient` that inherits from `LLMClient` and returns deterministic, hardcoded responses for testing purposes. It will be the default client for Phase 1.

- **`tasks.py`:**
    - A `load_task(client_id: str, task_id: str) -> BaseModel` function that reads the `task.json` and `prompts.jsonl` and returns the appropriate Pydantic model (`TextGenerationTask` or `ImageInformationExtractionTask`).
    - A `run_task(task: BaseModel, client: LLMClient, model: ModelConfig, evaluation_data: List[EvaluationData]) -> List[BenchmarkResult]` function that acts as a dispatcher. It checks the `task_type` and calls the appropriate handler (e.g., `_run_text_generation(...)`).

- **`runner.py`:**
    - The main `run_benchmark(client_id: str, task_id: str)` function.
    - **Enhanced Workflow:**
        1.  Loads the specified task using `tasks.load_task()`.
        2.  Loads and validates evaluation data using `data_manager.load_evaluation_data()`.
        3.  Loads the models to test against using `config.load_models()`.
        4.  Initialises the `FakeLLMClient`.
        5.  Iterates through each model.
        6.  For each model, calls `tasks.run_task()` with the evaluation data.
        7.  Applies privacy controls using `privacy.sanitize_results()`.
        8.  Collects all `BenchmarkResult` objects.
        9.  Saves the list of results to a timestamped JSON file in `results/`.

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
