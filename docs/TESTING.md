# Testing Guidelines

## Philosophy

We use a pragmatic, test-driven development (TDD) approach. Every new feature or bug fix must be accompanied by tests. We write tests first to define the desired behaviour, then write the code to make the tests pass.

Our goal is not 100% line coverage, but 100% confidence in the correctness of the core logic.

## Framework

- **Primary Framework:** `pytest` is the only test runner for this project.
- **Location:** All tests must be placed in the `/tests` directory.
- **File Naming:** Test files must be named `test_*.py` or `*_test.py`.
- **Test Naming:** Test functions must be prefixed with `test_`.

## How to Run Tests

Execute pytest from the root of the project:

```bash
pytest
```

To run tests for a specific file:

```bash
pytest tests/test_my_feature.py
```

## Types of Tests

1.  **Unit Tests:** These should be fast and isolated. They test a single function or class. Use mocks (`unittest.mock`) extensively to isolate components and avoid external dependencies like network calls or filesystem access.

2.  **Integration Tests:** These test the interaction between several components. They are allowed to be slower and have limited external dependencies (e.g., reading from the filesystem is acceptable, but making a real API call to an LLM is not).

3.  **E2E (End-to-End) Tests:** These test a full workflow, such as running the `1_run_benchmark.py` script and verifying the output file. These should be used sparingly and marked appropriately (`@pytest.mark.e2e`).

## Mocks vs. Fakes

- **Mocks (`unittest.mock`):** Use for isolating components in unit tests. For example, when testing a function that calls an LLM API, mock the API client.
- **Fakes (Hand-written classes):** Use for integration tests where a simple mock is insufficient. For example, we will use a `FakeLLMClient` that returns predictable, deterministic responses for testing the benchmark runner script.
