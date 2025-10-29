# .pre-commit-config.yaml in a target repo

```yaml
repos:
  - repo: https://github.com/you/precommit-validate-mypy-deps
    rev: v0.1.0
    hooks:
      - id: validate-mypy-deps
        always_run: true
```
