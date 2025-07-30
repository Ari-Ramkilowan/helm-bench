# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Helm Bench is a client-centered LLM evaluation platform designed to help consultants and developers find optimal model configurations for specific client tasks. The platform supports multiple task types including text generation and image extraction, with a modular architecture built around filesystem-based organization.

## Architecture

### Core Components
- **Data Models** (`src/helm_bench/data_models.py`): Pydantic models for tasks, results, and configurations
- **Data Manager** (`src/helm_bench/data_manager.py`): Central data loading, validation, and preparation
- **Privacy Controls** (`src/helm_bench/privacy.py`): Data sensitivity handling and access controls
- **Synthetic Data** (`src/helm_bench/synthetic.py`): Generate realistic fake data for testing
- **Template Engine** (`src/helm_bench/templates.py`): Pre-built evaluation scenarios for rapid setup
- **Task System** (`src/helm_bench/tasks.py`): Task dispatcher and handlers for different evaluation types
- **Runner** (`src/helm_bench/runner.py`): Main orchestration logic for benchmark execution
- **LLM Clients** (`src/helm_bench/llm_clients.py`): Abstract base and mock implementations for model interactions
- **Config** (`src/helm_bench/config.py`): Configuration loading and management

### Project Structure
- `datasets/<client_id>/<task_id>/`: Client-specific task definitions and data
  - `task.json`: Enhanced task definition with data source info, privacy level
  - `prompts.jsonl`: Prompt variations to test
  - `data/`: Input data, ground truth, metadata, validation schema
  - `images/`: For image_information_extraction tasks
- `datasets/templates/`: Reusable evaluation scenarios (contract_analysis, email_summarization, etc.)
- `datasets/generators/`: Synthetic data generation tools
- `results/`: Timestamped benchmark execution results
- `scripts/`: CLI entry points for the 3-phase workflow
- `src/helm_bench/`: Core business logic
- `tests/`: Comprehensive test suite following TDD principles

## Development Commands

### Environment Setup

**IMPORTANT**: This project uses uv for dependency management. Never use pip or manual venv activation.

```bash
# Initial setup (one-time per project)
uv venv --python 3.12
uv run setup

# That's it! No manual activation needed.
```

### Development Commands (Dev Script replaces Makefiles)

```bash
# Testing
./scripts/dev test              # Run all tests
./scripts/dev test-watch        # Run tests in watch mode

# Code Quality
./scripts/dev lint              # Check code style  
./scripts/dev format            # Format code
./scripts/dev lint-fix          # Fix auto-fixable issues
./scripts/dev check             # Run both lint and tests

# Project Scripts
./scripts/dev benchmark --client <id> --task <id>
./scripts/dev collect-votes
./scripts/dev generate-report

# Environment Management
./scripts/dev setup             # Reinstall dependencies
./scripts/dev clean             # Remove .venv (nuclear option)
```

**Key Rule**: Always use `./scripts/dev <command>` or `uv run <command>` - never run commands directly. This avoids Python PATH conflicts with Anaconda.

## Data Management

### Data Sources Support
- **Client Data**: Real, sensitive data with privacy controls
- **Synthetic Data**: Realistic fake data for testing scenarios  
- **Template Data**: Pre-built evaluation scenarios for common business cases
- **Public Data**: Benchmarking datasets for standardized comparisons

### Data Structure
Each task includes comprehensive data management:
```
data/
├── inputs.jsonl      # Input data for evaluation
├── expected.jsonl    # Ground truth (when available)
├── metadata.json     # Data provenance and privacy info
└── schema.json       # Data validation rules
```

### Privacy Levels
- **confidential**: Sensitive client data, restricted access
- **internal**: Company data, controlled access
- **public**: Open data, no restrictions

## Phase-Based Development

The project follows a 3-phase implementation:

1. **Phase 1**: Flexible Multi-Task Runner (`scripts/1_run_benchmark.py`)
   - Supports text_generation and image_extraction tasks
   - Uses mock LLM clients for development
   - Client/task-specific execution with `--client <id> --task <id>`

2. **Phase 2**: Evaluation Workbench (`scripts/2_collect_votes.py`)
   - Human-in-the-loop pairwise comparison
   - Model vs model and prompt vs prompt comparison modes

3. **Phase 3**: Reporting Engine (`scripts/3_generate_leaderboard.py`)
   - Client-specific ELO rankings and performance reports
   - Markdown output format

## Testing Philosophy

- **Test-Driven Development**: Write tests first, then implement
- **Three Test Types**:
  - Unit tests: Fast, isolated, heavily mocked
  - Integration tests: Component interaction testing
  - E2E tests: Full workflow validation (marked with `@pytest.mark.e2e`)
- Use `unittest.mock` for unit test isolation
- Use fake implementations (like `FakeLLMClient`) for integration tests

## Key Design Principles

- **Filesystem as Database**: All data organized in directory structure
- **Client-Centered**: Everything organized by client_id and task_id
- **Modular Task Types**: Extensible dispatcher pattern for different evaluation types
- **Mock-First Development**: Use deterministic fake clients before real API integration
- **Structured Results**: All outputs saved with clear metadata references

## Task Types

### Text Generation Tasks
- Standard prompt-in, text-out evaluation
- Defined in `datasets/<client>/<task>/task.json` with `task_type: "text_generation"`

### Image Information Extraction Tasks  
- Image + prompt input, text output evaluation
- Includes `image_path` field for multimodal evaluation
- Defined with `task_type: "image_information_extraction"`

## Important Files to Understand

- `docs/PRD_v1.md`: Complete product vision and requirements
- `specs/eval_tasks_phase_1_spec.md`: Detailed technical specification for Phase 1
- `docs/TESTING.md`: Comprehensive testing guidelines and philosophy
- `datasets/example_client/`: Example task structure and format
