from __future__ import annotations

import sys
from pathlib import Path

from ruamel.yaml import YAML


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines()]


def _clean(deps: list[str]) -> list[str]:
    return [d for d in deps if d and not d.startswith(("#", "-e"))]


def _get_mypy_deps(cfg_path: Path) -> list[str]:
    yaml = YAML(typ="safe")
    cfg = yaml.load(cfg_path.read_text()) or {}
    for repo in cfg.get("repos", []):
        if "mypy" not in repo.get("repo", ""):
            continue
        for hook in repo.get("hooks", []):
            if hook.get("id") == "mypy":
                return _clean(list(hook.get("additional_dependencies", [])))
    return []


def _set_mypy_deps(cfg_path: Path, deps: list[str]) -> bool:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    yaml.indent(mapping=2, sequence=4, offset=2)
    cfg = yaml.load(cfg_path.read_text()) or {}
    changed = False
    for repo in cfg.get("repos", []):
        if "mypy" not in repo.get("repo", ""):
            continue
        for hook in repo.get("hooks", []):
            if hook.get("id") == "mypy" and list(hook.get("additional_dependencies", [])) != deps:
                hook["additional_dependencies"] = deps
                changed = True
    if changed:
        yaml.dump(cfg, cfg_path.open("w"))
    return changed


def main() -> int:
    root = Path.cwd()  # pre-commit runs from the repo root
    req = _clean(_read_lines(root / "requirements.txt"))
    cfg_path = root / ".pre-commit-config.yaml"
    mypy_deps = _get_mypy_deps(cfg_path)

    if set(req) == set(mypy_deps):
        return 0

    if _set_mypy_deps(cfg_path, req):
        print("Updated mypy additional_dependencies from requirements.txt. Stage the changes and re-run.")
        return 1

    print("Sets differ but no hook updated. Check paths.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
