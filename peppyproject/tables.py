import warnings
from pathlib import Path
from typing import Any, Dict, List, Mapping, Union

import typepigeon

from peppyproject.base import ConfigurationTable, table_to_toml
from peppyproject.tools import CoverageTable, SetuptoolsTable
from peppyproject.tools.base import ToolTable


class ProjectMetadata(ConfigurationTable):
    """
    PEP621 project metadata configuration
    https://peps.python.org/pep-0621/#table-name
    """

    name = "project"
    fields = {
        "name": str,
        "version": str,
        "description": str,
        "readme": Union[Dict[str, str], str],
        "requires-python": str,
        "license": Dict[str, str],
        "authors": List[Dict[str, str]],
        "keywords": List[str],
        "classifiers": List[str],
        "urls": Dict[str, str],
        "scripts": Dict[str, str],
        "gui-scripts": Dict[str, str],
        "entry-points": Dict[str, Dict[str, str]],
        "dependencies": List[str],
        "optional-dependencies": Dict[str, List[str]],
        "dynamic": List[str],
    }

    def __setitem__(self, key: str, value: Any):
        generic = self.fields[key]
        directory = Path(
            self._ConfigurationTable__from_directory
            if hasattr(self, "_ConfigurationTable__from_directory")
            else "."
        )
        filenames = [filename.name for filename in directory.iterdir()]
        if value is not None:
            if key == "authors":
                if isinstance(value, str):
                    output_authors = []
                    input_authors = value.split(",")
                    for author in input_authors:
                        if "<" in author:
                            author, email = author.split("<")
                            email = email.split(">")[0]
                        else:
                            email = None
                        entry = {"name": author.strip()}
                        if email is not None:
                            entry["email"] = email.strip()
                        output_authors.append(entry)
                    value = output_authors
            elif key == "license":
                license_filename = None
                if isinstance(value, str) and value in filenames:
                    license_filename = value
                else:
                    license_files = [
                        filename
                        for filename in filenames
                        if "license" in filename.lower()
                    ]
                    if len(license_files) > 0:
                        if len(license_files) > 1:
                            warnings.warn(
                                f"multiple license files found; {license_files}"
                            )
                        license_filename = license_files[0]
                if license_filename is not None:
                    value = {"file": license_filename, "content-type": "text/plain"}
                else:
                    value = None
            elif key == "readme":
                if isinstance(value, Mapping) and "text" in value:
                    value = value["text"]
                if isinstance(value, str):
                    if value in filenames:
                        if Path(value).suffix.lower() == ".md":
                            content_type = "text/markdown"
                        else:
                            content_type = "text/x-rst"
                        value = {"file": value, "content-type": content_type}
                    else:
                        readme_files = [
                            filename
                            for filename in filenames
                            if "readme" in filename.lower()
                        ]
                        if len(readme_files) > 0:
                            if len(readme_files) > 1:
                                warnings.warn(
                                    f"multiple README files found; {readme_files}"
                                )
                            value = readme_files[0]
                        else:
                            value = {"text": value, "content-type": "text/plain"}
            elif key == "optional-dependencies":
                if not isinstance(value, generic.__origin__):
                    value = typepigeon.to_type(value, generic)
                for extra in value:
                    value[extra] = [
                        extra_dependency
                        for extra_dependency in typepigeon.to_type(
                            value[extra], generic.__args__[1]
                        )
                        if len(extra_dependency) > 0
                    ]
            elif key == "entry-points":
                if not isinstance(value, generic.__origin__):
                    value = typepigeon.to_type(value, generic)
                for entry_point_location in value:
                    entry_points = value[entry_point_location]
                    if isinstance(entry_points, str) and "=" in entry_points:
                        entry_points = [
                            tuple(entry.strip() for entry in entry_point.split("="))
                            for entry_point in entry_points.splitlines()
                            if len(entry_point) > 0
                        ]
                        value[entry_point_location] = {
                            key: value for key, value in entry_points
                        }

        super().__setitem__(key, value)


class BuildConfiguration(ConfigurationTable):
    """
    PEP517 build system configuration
    https://peps.python.org/pep-0517/#source-trees
    """

    name = "build-system"
    fields = {
        "requires": List[str],
        "build-backend": str,
    }


class ToolsTable(ConfigurationTable):
    """
    abstraction of the top-level ``[tool]`` table in ``pyproject.toml``
    """

    name = "tool"
    fields = {
        "setuptools": SetuptoolsTable,
        "coverage": CoverageTable,
    }
    start_with_placeholders = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setitem__(self, table_name: str, table: "ToolTable"):
        if (
            table_name in self.fields
            and self.fields[table_name] is not None
            and table is not None
        ):
            configuration = self.fields[table_name]()
            configuration.update(table)
            table = configuration
        super().__setitem__(key=table_name, value=table)

    def update(self, items: Mapping):
        for key, value in items.items():
            if value is not None:
                if (
                    key in self
                    and isinstance(self[key], Mapping)
                    and isinstance(value, Mapping)
                ):
                    self[key].update(value)
                else:
                    self[key] = value

    def to_toml(self) -> str:
        tables = self._ConfigurationTable__configuration
        for table_name, table in tables.items():
            if isinstance(table, ConfigurationTable):
                tables[table_name] = {
                    key: value for key, value in table.items() if value is not None
                }
        return table_to_toml(table_name="tool", table=tables)
