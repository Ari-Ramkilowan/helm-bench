# Git Workflow Guidelines

## Branching Strategy

We use a simple feature-branching workflow.

- **`main`:** This branch is the source of truth. It must always be stable and deployable. Direct pushes to `main` are forbidden.
- **Feature Branches:** All new work (features, bug fixes) must be done on a feature branch. Branches should be named descriptively using the format `[type]/[short-description]`, for example:
    - `feature/add-image-extraction-task`
    - `bugfix/fix-result-parsing-error`
    - `docs/update-prd-v2`

## The Workflow

1.  **Create a Branch:** Before starting work, pull the latest changes from `main` and create a new feature branch:
    ```bash
    git checkout main
    git pull origin main
    git checkout -b feature/my-new-feature
    ```

2.  **Commit Changes:** Make small, atomic commits. Write clear and concise commit messages following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

    - **Format:** `feat: add user authentication endpoint`
    - **Scope (Optional):** `feat(api): add user authentication endpoint`
    - **Breaking Change:** `refactor!: drop support for Python 3.11`

3. Make sure all tests pass before creating a PR

4. **Create a Pull Request (PR):** When your feature is complete and tested, push your branch to the remote and open a Pull Request against the `main` branch.

    - The PR description should clearly explain the **"why"** behind the changes. Link to any relevant issues or PRDs.

5  **Code Review:** At least one other **person** must review and approve the PR before it can be merged.

6  **Merge:** Once approved and all checks have passed, merge the PR into `main` using a **squash and merge**. This keeps the `main` branch history clean and readable.

# Commit Message Style Guide

We follow the Conventional Commits specification. This helps with automated versioning and changelog generation.

**Examples:**

- **`feat:`** A new feature.
  ```
  feat: allow users to upload a profile picture
  ```
- **`fix:`** A bug fix.
  ```
  fix: prevent race condition when creating accounts
  ```
- **`docs:`** Documentation only changes.
  ```
  docs: update TESTING.md with e2e guidelines
  ```
- **`style:`** Changes that do not affect the meaning of the code (white-space, formatting, etc).
  ```
  style: format all python files with black
  ```
- **`refactor:`** A code change that neither fixes a bug nor adds a feature.
  ```
  refactor: extract user repository from auth service
  ```
- **`test:`** Adding missing tests or correcting existing tests.
  ```
  test: add unit tests for the new payment gateway
  ```
- **`chore:`** Changes to the build process or auxiliary tools.
  ```
  chore: add new linter rule
  ```
