from typing import List

from peppyproject.tools.base import ToolTable


class CoverageTable(ToolTable):
    name = "tool.coverage"
    fields = {
        "run": {
            "omit": List[str],
        },
        "report": {
            "exclude_lines": List[str],
        },
    }
