from typing import Any, Dict, List, Union

from peppyproject.tools.base import ToolTable


class SetuptoolsTable(ToolTable):
    """
    ``setuptools`` configuration
    https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#setuptools-specific-configuration
    """

    name = "tool.setuptools"
    fields = {
        "platforms": List[str],
        # If not specified, ``setuptools`` will try to guess a reasonable default for the package
        "zip-safe": bool,
        "eager-resources": List[str],
        "py-modules": List[str],
        "packages": Union[List[str], Dict[str, Any]],
        # Used when explicitly listing ``packages``
        "package-dir": Union[Dict[str, Any]],
        # See https://setuptools.pypa.io/en/latest/userguide/datafiles.html
        "package-data": Dict[str, List[str]],
        # ``True`` by default
        "include-package-data": bool,
        "exclude-package-data": Dict[str, List[str]],
        # Provisional - likely to change with PEP 639 (by default: ``['LICEN[CS]E*', 'COPYING*', 'NOTICE*', 'AUTHORS*']``)
        "license-files": List[str],
    }
