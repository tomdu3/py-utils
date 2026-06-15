# Personal Python Utilities

## Utilities

### Image to Sketch

Converts an image to a sketch. Usage: `uv run utils/image2sketch.py <image_path>` or it can be used as a module: `from utils.image2sketch import image2sketch`

### Image to ASCII

Converts an image to ASCII art. Usage: `uv run utils/image2ascii.py <image_path>` or it can be used as a module: `from utils.image2ascii import image2ascii`

### GitHub Stats Retriever

Retrieves and displays statistics for a GitHub user and their repositories.
Usage:
```bash
uv run utils/github_stats.py [username]
```
Options:
- `-t, --token <token>`: Provide a GitHub Personal Access Token (or set `GITHUB_TOKEN` environment variable) to avoid API rate limits.
- `-l, --limit <count>`: Limit the number of repositories shown (default: 5).

Can also be used as a module:
```python
from utils.github_stats import fetch_github_user, fetch_github_repos
```
See the detailed guide in [docs/github_stats.md](file:///home/tom/projects/py-utils/docs/github_stats.md) for more details.

## Development Tools & Workflow

This project includes industry-standard development tools configured to run inside the local virtual environment. For a complete guide on how they are configured, their benefits, and advanced usage, see [docs/dev_tools.md](file:///home/tom/projects/py-utils/docs/dev_tools.md).

### 1. Code Style, Linting & Formatting (Ruff)
We use [Ruff](https://github.com/astral-sh/ruff) to enforce code format and PEP 8 guidelines.

*   **Linting Check:** `uv run ruff check .`
*   **Auto-Fix Lint Errors:** `uv run ruff check --fix .`
*   **Formatting Check:** `uv run ruff format --check .`
*   **Auto-Format Code:** `uv run ruff format .`

### 2. Testing (`pytest`)
We use `pytest` for unit testing and `pytest-cov` to generate code coverage statistics.

*   **Run All Tests:**
    ```bash
    uv run pytest
    ```
*   **Run Tests with Coverage Report:**
    ```bash
    uv run pytest --cov=utils --cov-report=term-missing
    ```

### 3. Static Type Checking (`mypy`)
We use `mypy` to verify Python type annotations and catch bugs early.

*   **Run Type Checking:**
    ```bash
    uv run mypy utils/
    ```

### 4. Git Pre-commit Hooks (`pre-commit`)
Pre-commit hooks are configured to run automatically before every git commit to ensure no broken or unformatted code is added to the repository history.
The hooks include:
*   Standard sanity checks (trailing whitespace, end-of-file fixers, YAML checkers).
*   Ruff auto-formatting and linting.
*   Mypy type checking.

*   **Install Hooks (One-time setup):**
    ```bash
    uv run pre-commit install
    ```
*   **Run Hooks Manually (on all files):**
    ```bash
    uv run pre-commit run --all-files
    ```

### 5. Interactive Debugging & Scratchpad (`ipython`)
For quick testing and experimenting with the code or libraries (e.g. testing `requests` payload outputs), use IPython:
```bash
uv run ipython
```

## Resources

- [Convert your image to ASCII art using Python](https://www.youtube.com/watch?v=cjZYvJRtGXg)
- [How to create an image to ASCII converter in Python](https://youtu.be/cjZYvJRtGXg)
- [Turn any image into ASCII art](https://youtu.be/v_raWlX7tZY)
