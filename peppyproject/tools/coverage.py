from peppyproject.tools.base import ToolTable


class CoverageTable(ToolTable):
    name = "tool.coverage"
    fields = {
        "run": {
            "branch": bool,
            "command_line": str,
            "concurrency": list[str],
            "context": str,
            "cover_pylib": bool,
            "data_file": str,
            "disable_warnings": bool,
            "debug": list[str],
            "dynamic_context": str,
            "include": list[str],
            "omit": list[str],
            "parallel": bool,
            "plugins": list[str],
            "relative_files": bool,
            "sigterm": bool,
            "source": list[str],
            "source_pkgs": list[str],
            "timid": bool,
        },
        "paths": dict[str, list[str]],
        "report": {
            "exclude_lines": list[str],
            "fail_under": float,
            "ignore_errors": bool,
            "include": list[str],
            "omit": list[str],
            "partial_branches": list[str],
            "precision": int,
            "show_missing": bool,
            "skip_covered": bool,
            "skip_empty": bool,
            "sort": str,
        },
        "html": {
            "directory": str,
            "extra_css": str,
            "show_contexts": bool,
            "skip_covered": bool,
            "skip_empty": bool,
            "title": str,
        },
        "xml": {
            "output": str,
            "package_depth": int,
        },
        "json": {
            "output": str,
            "pretty_print": bool,
            "show_contexts": bool,
        },
        "lcov": {
            "output": str,
        },
    }
