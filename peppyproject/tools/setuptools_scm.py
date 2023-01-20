from pathlib import Path
from typing import Any

from peppyproject.tools.base import ToolTable


class SetuptoolsSCMTable(ToolTable):
    name = "tool.setuptools_scm"
    fields = {
        "root": Path,
        "version_scheme": str,
        "local_scheme": str,
        "write_to": Path,
        "write_to_template": str,
        "relative_to": str,
        "tag_regex": str,
        "parentdir_prefix_version": str,
        "fallback_version": str,
        "fallback_root": Path,
        "parse": Any,
        "git_describe_command": Any,
        "dist_name": str,
        "version_cls": Any,
        "normalize": bool,
        "search_parent_directories": bool,
    }
