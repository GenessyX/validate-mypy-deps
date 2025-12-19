# Validate mypy deps pre-commit hook.

## Description

This hook can be used to avoid manual synchronization of mypy hook additional_dependencies. By default it reads `requirements.txt` in the repository root, but you can point it to any requirements file with `--requirements-path`.

### Hook set up:

```yaml
repos:
  - repo: https://github.com/GenessyX/validate-mypy-deps
    rev: v0.1.1
    hooks:
      - id: validate-mypy-deps
        always_run: true
        # Example: override requirements location
        # args: ["--requirements-path", "requirements/dev.txt"]
```

### UV set up:

If you are using uv, dependencies can be exported directly from lockfile using this pre-commit hook:

```yaml
repos:
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.6.10
    hooks:
      - id: uv-export
        args: ["--format", "requirements-txt", "--no-hashes", "--frozen", "--output-file", "requirements.txt"]
        always_run: true

  - repo: https://github.com/GenessyX/validate-mypy-deps
    rev: v0.1.1
    hooks:
      - id: validate-mypy-deps
        always_run: true
```
