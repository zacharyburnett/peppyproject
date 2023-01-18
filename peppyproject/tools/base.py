from abc import ABC
from typing import Any

from peppyproject.base import ConfigurationTable


class ToolTable(ConfigurationTable, ABC):
    """
    abstraction of an individual tool configuration
    """

    def __init__(self, **kwargs: dict[str, Any]):
        super().__init__(**kwargs)
        if self.name is not None and not self.name.startswith("tool."):
            message = f'"{self.name}" table name must start with `tool.`'
            raise ValueError(message)
