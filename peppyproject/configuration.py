from pathlib import Path
from typing import Iterator, Mapping

from peppyproject.base import ConfigurationTable
from peppyproject.tables import BuildConfiguration, ProjectMetadata, ToolsTable
from peppyproject.tools.setuptools_scm import SetuptoolsSCMTable


class PyProjectConfiguration(Mapping):
    """
    abstraction of ``pyproject.toml`` configuration
    """

    def __init__(
        self,
        project: ProjectMetadata = None,
        build_system: BuildConfiguration = None,
        tool: ToolsTable = None,
    ):
        if project is None or len(project) == 0:
            project = ProjectMetadata()
        if tool is None or len(tool) == 0:
            tool = ToolsTable()
        if build_system is None or len(build_system) == 0:
            build_system = BuildConfiguration.default_setuptools()
        if project["dynamic"] is not None and "version" in project["dynamic"]:
            if not any(
                "setuptools_scm" in requirement
                for requirement in build_system["requires"]
            ):
                build_system["requires"].append("setuptools_scm[toml]>=3.4")
                if "setuptools_scm" not in tool:
                    tool["setuptools_scm"] = SetuptoolsSCMTable()
        self.__tables = {
            "project": project,
            "build-system": build_system,
            "tool": tool,
        }

    @classmethod
    def from_directory(cls, directory: str) -> "PyProjectConfiguration":
        if not isinstance(directory, Path):
            directory = Path(directory)

        return cls(
            project=ProjectMetadata.from_directory(directory=directory),
            build_system=BuildConfiguration.from_directory(directory=directory),
            tool=ToolsTable.from_directory(directory=directory),
        )

    def __getitem__(self, table: str) -> ConfigurationTable:
        return self.__tables[table]

    @property
    def configuration(self) -> str:
        return "\n".join(table.configuration for table in self.__tables.values())

    def to_file(self, filename: str):
        with open(filename, "w") as configuration_file:
            configuration_file.write(self.configuration)

    def __len__(self) -> int:
        return len(self.__tables)

    def __iter__(self) -> Iterator:
        yield from self.__tables

    def __repr__(self) -> str:
        tables_string = ", ".join(
            f"{key}={repr(value)}"
            for key, value in self.__tables.items()
            if value is not None and (not hasattr(value, "__len__") or len(value) > 0)
        )
        return f"{self.__class__.__name__}({tables_string})"
