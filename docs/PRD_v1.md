# Product Requirements Document (PRD) - v1.0
# Helm: The Client-Centred LLM Evaluation Platform

**Author:** Ari (via Gemini)
**Version:** 1.0
**Date:**  July 2025
**Status:** Proposed

---

## 1. Introduction & Vision

In the rapidly evolving landscape of Large Language Models, businesses need more than generic benchmarks. They require a robust, empirical way to determine which models and which prompts will perform best for their specific, mission-critical tasks.

**Helm** is envisioned as a client-centred, modular LLM evaluation platform. It moves beyond public leaderboards to provide a private, powerful workbench for LLMOps. It will empower consultants and developers to conduct rigorous, repeatable experiments to find the optimal configuration (model + prompt + guardrails) for any given client task, from text generation and RAG to multimodal analysis.

## 2. The Problem

A client wants to use LLMs to improve their business processes. They face several critical questions:
- Which of the dozens of available models (OpenAI, Anthropic, Google, open-source) is the most reliable and performant *for my specific needs*?
- How do I craft the perfect prompt to get the desired output for a task?
- How can I test a model's performance on complex tasks, like extracting information from internal documents (RAG) or analysing images?
- How do I ensure a model adheres to our company's safety and bias guardrails?
- How do I track performance over time as new models are released?

Answering these questions currently involves ad-hoc scripting, manual data collection, and a lack of standardised process, leading to inconsistent and unreliable results.

## 3. Goals & Objectives

### Business Goals
- **Enable Data-Driven Consulting:** Provide an empirical foundation for recommending specific LLM solutions to clients.
- **Increase Development Efficiency:** Accelerate the process of prompt engineering and model selection.
- **Create a Reusable Asset:** Build a flexible platform that can be adapted for any client and any LLM-based task.

### Product Goals
- **Phase 1 (Core Task Runner):** Build a flexible engine that can run different types of evaluation tasks (text, image) organised by client.
- **Phase 2 (Evaluation Workbench):** Create a CLI-based tool for human-in-the-loop, pairwise comparison of task outputs.
- **Phase 3 (Reporting Engine):** Generate client-specific reports, including model ELO rankings and prompt performance analysis.
- **Future Phases:** Incorporate more complex task types like RAG, bias testing, and guardrail adherence.

## 4. User Personas

- **LLM Consultant/Developer (Primary User):** Designs and runs the evaluations. They define client tasks, configure the models to be tested, and analyse the results to provide recommendations.
- **Client Stakeholder (End User):** Consumes the final reports to understand which model and prompt combination is the best investment for their business objective.

## 5. Features & Requirements

### 5.1. Core Architecture
- **Client-Centred Directory Structure:** The filesystem will be the database. All assets for a given evaluation will be organised by client and task: `datasets/<client_id>/<task_id>/`.
- **Enhanced Task Definition:** Each task directory contains:
  - `task.json`: Task type, data source info, privacy level, evaluation criteria
  - `prompts.jsonl`: Prompt variations to test
  - `data/`: Input data, optional ground truth, metadata, validation schema
  - `images/`: For image_information_extraction tasks
- **Flexible Data Sources:** Support for client data, synthetic data, templates, and public datasets with appropriate privacy controls.
- **Data Templates:** Reusable evaluation scenarios (`templates/contract_analysis/`, `templates/email_summarization/`) for rapid setup.
- **Synthetic Data Generation:** Tools to create realistic but fake data when client data is unavailable or too sensitive.
- **Modular Task Runners:** Dispatcher system with enhanced data handling capabilities.

### 5.2. Data Management Requirements
- **Privacy Controls:** Handle confidential, internal, and public data appropriately with clear metadata tracking.
- **Data Validation:** Ensure input data meets schema requirements and quality standards.
- **Template System:** Pre-built evaluation datasets for common business scenarios (contract analysis, email summarization, document Q&A, customer support).
- **Synthetic Data Generation:** Create realistic but fake data for testing when real data is unavailable or too sensitive.
- **Ground Truth Handling:** Support optional expected outputs for automated quality metrics alongside human evaluation.
- **Data Import Tools:** Support common formats (JSON, JSONL, CSV, images) with validation and conversion capabilities.

### 5.3. Phase 1: Enhanced Benchmark Runner
- **CLI Entry Point:** A primary script `scripts/1_run_benchmark.py`.
- **Arguments:** The script must accept `--client <client_id>` and `--task <task_id>` to specify which evaluation to run.
- **Data Preparation:** Load and validate evaluation data from multiple sources (client, synthetic, template).
- **Task Support:** Must support at least two task types initially:
    - `text_generation`: Standard prompt-in, text-out with configurable input data.
    - `image_information_extraction`: Image-and-prompt-in, text-out with image dataset support.
- **Mock Models:** Initial development will be against mock LLM clients to simulate API calls for both text and vision models without incurring costs.
- **Structured Results:** All results must be saved to a timestamped file in the `results/` directory, containing clear references to `client_id`, `task_id`, `prompt_id`, `model_id`, and data provenance.

### 5.4. Phase 2: Multimodal Evaluation Workbench
- **CLI Entry Point:** `scripts/2_collect_votes.py`.
- **Dual Comparison Modes:** The script must support two modes for pairwise voting:
    - **Model vs. Model:** For a fixed prompt, compare the outputs of two different models.
    - **Prompt vs. Prompt:** For a fixed model, compare the outputs from two different prompt variations.
- **Multimodal Context:** When evaluating an image task, the CLI must display the path to the source image to provide context for the voter.
- **Vote Storage:** Votes must be saved in a structured format that links back to the original results.

### 5.5. Phase 3: Client-Centric Reporting
- **CLI Entry Point:** `scripts/3_generate_leaderboard.py`.
- **Client-Specific Filtering:** The script must be able to generate a report for a single client using a `--client <client_id>` flag.
- **Multi-Dimensional Reports:** The output (in Markdown format) must include:
    - An overall ELO rating and leaderboard for all models tested for that client.
    - A breakdown of model performance by task type.
    - A per-task ranking of prompt effectiveness based on win/loss ratios.

## 6. Out of Scope (For v1.0)

- **Graphical User Interface (GUI):** The entire v1.0 will be CLI-based. A web interface is a potential future enhancement.
- **Automated Evaluation Metrics:** Initial evaluation will be purely human-in-the-loop (pairwise voting). Metrics like ROUGE, BLEU, etc., are not part of the initial scope.
- **Direct Database Integration:** The filesystem will serve as the primary data store. Integration with a formal database like PostgreSQL or SQLite is out of scope for v1.0.
- **Real-time/Streaming Data:** All tasks are batch-processed.

## 7. Success Metrics

- **Phase 1:** A developer can successfully define and run both a text and an image task for a new client through the CLI.
- **Phase 2:** A user can load the results from Phase 1 and cast votes to compare model and prompt performance.
- **Phase 3:** The system can generate a coherent, multi-faceted report in Markdown that clearly shows which models and prompts are winning for a specific client's tasks.
