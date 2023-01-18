
from peppyproject.tools.base import ToolTable


class CoverageTable(ToolTable):
    name = "tool.coverage"
    fields = {
        "run": {
            "omit": list[str],
        },
        "report": {
            "exclude_lines": list[str],
        },
    }
