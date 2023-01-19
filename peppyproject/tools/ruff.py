from pathlib import Path

from peppyproject.tools.base import ToolTable


class RuffTable(ToolTable):
    """
    ``ruff`` configuration
    https://github.com/charliermarsh/ruff#reference
    """

    name = "tool.ruff"
    fields = {
        "allowed-confusables": list[str],
        "builtins": list[str],
        "cache-dir": str,
        "dummy-variable-rgx": str,
        "exclude": list[str],
        "extend": str,
        "extend-exclude": list[str],
        "extend-ignore": list[str],
        "extend-select": list[str],
        "external": list[str],
        "fix": bool,
        "fix-only": bool,
        "fixable": list[str],
        "force-exclude": bool,
        "format": str,
        "ignore": list[str],
        "ignore-init-module-imports": bool,
        "line-length": int,
        "namespace-packages": list[str],
        "per-file-ignores": dict[str, list[str]],
        "required-version": str,
        "respect-gitignore": bool,
        "select": list[str],
        "show-source": bool,
        "src": list[Path],
        "target-version": str,
        "task-tags": list[str],
        "typing-modules": list[str],
        "unfixable": list[str],
        "update-check": bool,
        "flake8-annotations": {
            "allow-star-arg-any": bool,
            "mypy-init-return": bool,
            "suppress-dummy-args": bool,
            "suppress-none-returning": bool,
        },
        "flake8-bandit": {
            "hardcoded-tmp-directory": list[str],
            "hardcoded-tmp-directory-extend": list[str],
        },
        "flake8-bugbear": {
            "extend-immutable-calls": list[str],
        },
        "flake8-errmsg": {
            "max-string-length": int,
        },
        "flake8-import-conventions": {
            "aliases": dict[str, str],
            "extend-aliases": dict[str, str],
        },
        "flake8-pytest-style": {
            "fixture-parentheses": bool,
            "mark-parentheses": bool,
            "parametrize-names-type": str,
            "parametrize-values-row-type": str,
            "parametrize-values-type": str,
            "raises-extend-require-match-for": list[str],
            "raises-require-match-for": list[str],
        },
        "flake8-quotes": {
            "avoid-escape": bool,
            "docstring-quotes": str,
            "inline-quotes": str,
            "multiline-quotes": str,
        },
        "flake8-tidy-imports": {
            "ban-relative-imports": str,
            "banned-api": dict[str, str],
        },
        "flake8-unused-arguments": {
            "ignore-variadic-names": bool,
        },
        "isort": {
            "classes": list[str],
            "combine-as-imports": bool,
            "constants": list[str],
            "extra-standard-library": list[str],
            "force-single-line": bool,
            "force-sort-within-sections": bool,
            "force-wrap-aliases": bool,
            "known-first-party": list[str],
            "known-third-party": list[str],
            "no-lines-before": list[str],
            "order-by-type": bool,
            "relative-imports-order": str,
            "required-imports": list[str],
            "single-line-exclusions": list[str],
            "split-on-trailing-comma": bool,
            "variables": list[str],
        },
        "mccabe": {
            "max-complexity": int,
        },
        "pep8-naming": {
            "classmethod-decorators": list[str],
            "ignore-names": list[str],
            "staticmethod-decorators": list[str],
        },
        "pycodestyle": {
            "ignore-overlong-task-comments": bool,
            "max-doc-length": int,
        },
        "pydocstyle": {
            "convention": str,
        },
        "pyupgrade": {
            "keep-runtime-typing": bool,
        },
    }
