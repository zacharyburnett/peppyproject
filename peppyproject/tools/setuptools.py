from typing import Any, Union

from peppyproject.tools.base import ToolTable


class SetuptoolsTable(ToolTable):
    """
    ``setuptools`` configuration
    https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#setuptools-specific-configuration
    """

    name = "tool.setuptools"
    fields = {
        "platforms": list[str],
        # If not specified, ``setuptools`` will try to guess a reasonable default for the package
        "zip-safe": bool,
        "eager-resources": list[str],
        "py-modules": list[str],
        "packages": Union[list[str], dict[str, Any], str],
        # Used when explicitly listing ``packages``
        "package-dir": Union[dict[str, Any]],
        # See https://setuptools.pypa.io/en/latest/userguide/datafiles.html
        "package-data": dict[str, list[str]],
        # ``True`` by default
        "include-package-data": bool,
        "exclude-package-data": dict[str, list[str]],
        # Provisional - likely to change with PEP 639 (by default: ``['LICEN[CS]E*', 'COPYING*', 'NOTICE*', 'AUTHORS*']``)
        "license-files": list[str],
    }
