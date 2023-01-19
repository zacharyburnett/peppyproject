from peppyproject.tools.base import ToolTable


class Flake8Table(ToolTable):
    """
    ``flake8`` configuration
    https://flake8.pycqa.org/en/latest/user/options.html#options-and-their-descriptions
    """

    name = "tool.flake8"
    fields = {
        "quiet": int,
        "count": bool,
        "exclude": list[str],
        "extend-exclude": list[str],
        "filename": list[str],
        "format": str,
        "hang-closing": bool,
        "ignore": list[str],
        "extend-ignore": list[str],
        "max-line-length": int,
        "max-doc-length": int,
        "indent-size": int,
        "select": list[str],
        "extend-select": list[str],
        "disable-noqa": bool,
        "show-source": bool,
        "statistics": bool,
        "require-plugins": list[str],
        "enable-extensions": list[str],
        "jobs": int,
        "tee": bool,
        "builtins": list[str],
        "doctests": bool,
        "include-in-doctest": list[str],
        "exclude-from-doctest": list[str],
        "max-complexity": int,
    }
