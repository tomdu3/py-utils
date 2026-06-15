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

## Code Style and Formatting

This repository follows PEP 8 styling guidelines. We use [Ruff](https://github.com/astral-sh/ruff) to enforce code format and rules.

### Linting
To check for PEP 8 compliance and other lint errors:
```bash
uvx ruff check .
```

To automatically fix safe lint errors:
```bash
uvx ruff check --fix .
```

### Formatting
To verify files are formatted correctly:
```bash
uvx ruff format --check .
```

To automatically format the codebase:
```bash
uvx ruff format .
```


## Resources

- [Convert your image to ASCII art using Python](https://www.youtube.com/watch?v=cjZYvJRtGXg)
- [How to create an image to ASCII converter in Python](https://youtu.be/cjZYvJRtGXg)
- [Turn any image into ASCII art](https://youtu.be/v_raWlX7tZY)