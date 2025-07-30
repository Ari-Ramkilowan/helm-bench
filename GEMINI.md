# Helm Bench: Client-Centred LLM Evaluation Platform

This project is a comprehensive, client-centred platform for evaluating and optimising Large Language Models (LLMs). Its primary purpose is to move beyond generic benchmarks and provide actionable insights for specific client use cases.

The platform is designed to be a powerful **LLMOps and Evaluation Workbench**.

## Core Objectives

1.  **Client-Centred Organisation:** All evaluation tasks, data, and results are organised by client, allowing for tailored analysis and reporting.
2.  **Diverse Task Support:** The system is architected to handle a wide variety of evaluation tasks, including:
    *   Text Generation
    *   Multimodal Information Extraction (e.g., from images)
    *   Retrieval-Augmented Generation (RAG) performance
    *   Bias and Fairness testing
    *   Guardrail and Safety adherence
3.  **Dual Optimisation:** The platform is built to answer two key questions simultaneously:
    *   **Which model is best?** (For a specific client or task)
    *   **Which prompt is best?** (For a specific task and model)
4.  **Actionable Reporting:** The ultimate output is not just a leaderboard, but a detailed set of reports that provide client-specific insights, enabling data-driven decisions on model selection and prompt engineering.

## Development Philosophy

- **Test-Driven Development (TDD):** Ensures code quality, correctness, and maintainability.
- **Modular Architecture:** Core logic is separated from scripts to promote reusability and scalability.
- **Phased Rollout:** Features are developed in distinct, iterative phases, each delivering concrete value.

---

# Project Assistant Guidelines

## Project Overview
- **Purpose:** LLM benchmarking and evaluation platform
- **Tech Stack:** FastAPI, Python 3.12, UV package management
- **Architecture:** @./docs/ARCHITECTURE.md

## Quick Reference
- **Testing:** Always use pytest → @./docs/TESTING.md
- **Git Workflow:** → @./docs/GIT.md
- **Code Style:** → @./docs/STYLE.md
- **API Design:** → @./docs/API.md

## Core Principles
- Pragmatic over perfect
- Real business metrics over vanity metrics
- Documentation as code
- Fail fast, learn faster

## Key Context
- ELO rating system for model comparison
- Custom evaluation frameworks (not generic benchmarks)
- Budget-conscious infrastructure choices
- Trust-scored information retrieval

## Common Patterns
- **Dispatcher/Handler Pattern for Tasks:** For running different evaluation types, use a central dispatcher. The main script calls the dispatcher, which reads the `task.json` and delegates to a specific `handle_text_generation_task()` or `handle_image_extraction_task()` function. This keeps the main script clean and makes it easy to add new task types.
- **Configuration via Pydanitc:** Instead of passing loose variables, group related configurations into Pydantic models or dataclasses (e.g., a `ModelConfig` class that holds `name`, `api_key`, `endpoint`). This provides type safety and makes function signatures cleaner.
Always use Typehinting.

## Don't Do This
- **Avoid Hardcoding in Scripts:** Never hardcode model names, API keys, or prompts directly into the Python code. All configuration must be loaded from `config/` files and all prompts/datasets from the `datasets/` directory. This ensures the platform is flexible.
- **Avoid Logic in Top-Level Scripts:** The scripts in the `scripts/` directory should be thin wrappers. Their only job is to parse arguments and call the core application logic (which should live in a `src/` directory). Do not put complex business logic, data processing, or model interaction code directly into these scripts.
