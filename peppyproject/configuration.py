from os import PathLike
from pathlib import Path
from typing import Mapping, Iterator

from peppyproject.tables import (
    ConfigurationTable,
    ProjectMetadata,
    BuildConfiguration,
    ToolTable,
)


class PyProjectConfiguration(Mapping):
    """
    abstraction of ``pyproject.toml`` configuration
    """

    def __init__(
            self,
            project: ProjectMetadata = None,
            build_system: BuildConfiguration = None,
            tool: ToolTable = None,
    ):
        if project is None:
            project = ProjectMetadata()
        if build_system is None:
            build_system = BuildConfiguration()
        if tool is None:
            tool = ToolTable()
        self.__tables = {
            "project": project,
            "build-system": build_system,
            "tool": tool,
        }

    @classmethod
    def from_directory(cls, directory: PathLike) -> "PyProjectConfiguration":
        if not isinstance(directory, Path):
            directory = Path(directory)

        return cls(
            project=ProjectMetadata.from_directory(directory=directory),
            build_system=BuildConfiguration.from_directory(directory=directory),
            tool=ToolTable.from_directory(directory=directory),
        )

    def __getitem__(self, table: str) -> ConfigurationTable:
        return self.__tables[table]

    def __len__(self) -> int:
        return len(self.__tables)

    def __iter__(self) -> Iterator:
        yield from self.__tables

    def __repr__(self) -> str:
        tables_string = ", ".join(
            f"{key}={repr(value)}"
            for key, value in self.__tables.items()
            if value is not None
        )
        return f"{self.__class__.__name__}({tables_string})"
