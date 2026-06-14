# Personal Python Utilities

## Utilities

### Image to Sketch

Converts an image to a sketch. Usage: `uv run utils/image2sketch.py <image_path>` or it can be used as a module: `from utils.image2sketch import image2sketch`

### Image to ASCII

Converts an image to ASCII art. Usage: `uv run utils/image2ascii.py <image_path>` or it can be used as a module: `from utils.image2ascii import image2ascii`

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