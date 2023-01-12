import warnings
from abc import ABC
from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from typing import MutableMapping, Dict, Any, Mapping, Iterator, Union, List

import tomli
import typepigeon

from peppyproject.files import SETUP_CFG, read_setup_py


class ConfigurationTable(MutableMapping, ABC):
    """
    abstraction of a TOML configuration table
    """

    name: str
    fields: Dict[str, Any]
    start_with_placeholders: bool = True

    def __init__(self, **kwargs):
        if self.start_with_placeholders:
            self.__configuration = {key: None for key in self.fields}
        else:
            self.__configuration = {}
        if len(kwargs) > 0:
            self.update(kwargs)

    @classmethod
    def from_file(cls, filename: PathLike) -> "ConfigurationTable":
        if not isinstance(filename, Path):
            filename = Path(filename)

        configuration = cls()
        configuration.__from_directory = filename.parent
        if filename.name.lower() == "pyproject.toml":
            with open(filename, "rb") as configuration_file:
                file_configuration = tomli.load(configuration_file)
            base_table = cls.name.split(".", 1)[0]
            if base_table in file_configuration:
                configuration.update(file_configuration[base_table])
        elif filename.name.lower() == "setup.cfg":
            setup_cfg = ConfigParser()
            setup_cfg.read([filename])
            for section in setup_cfg:
                if "." not in section:
                    section_translations = (
                        SETUP_CFG[section] if section in SETUP_CFG else None
                    )
                    for key, value in setup_cfg.items(section):
                        if (
                            section_translations is not None
                            and key in section_translations
                        ):
                            table, entry = section_translations[key].rsplit(".", 1)
                            if table == cls.name:
                                value = [
                                    line for line in value.splitlines() if len(line) > 0
                                ]
                                if len(value) == 1:
                                    value = value[0]
                                configuration[entry] = value
                else:
                    values = setup_cfg.items(section)
                    if section in ["options.extras_require", "options.entry_points"]:
                        values = dict(values)
                    section, key = section.split(".", 1)
                    if section in SETUP_CFG:
                        section_translations = SETUP_CFG[section]
                        if key in section_translations:
                            table, entry = section_translations[key].rsplit(".", 1)
                            if table == cls.name:
                                configuration[entry] = values
        elif filename.name.lower() == "setup.py":
            setup_py = read_setup_py(filename)
            for section, section_translations in SETUP_CFG.items():
                for key, value in setup_py.items():
                    if key in section_translations:
                        table, entry = section_translations[key].rsplit(".", 1)
                        tables = table.split(".")
                        if tables[0] == cls.name:
                            if len(tables) > 1:
                                configuration[tables[1]][entry] = value
                            else:
                                configuration[entry] = value

        return configuration

    @classmethod
    def from_directory(cls, directory: PathLike) -> "ConfigurationTable":
        if not isinstance(directory, Path):
            directory = Path(directory)

        known_configuration_filenames = ["pyproject.toml", "setup.cfg", "setup.py"]

        file_configurations = {}
        for filename in directory.iterdir():
            if filename.is_file():
                if filename.name in known_configuration_filenames:
                    file_configuration = cls.from_file(filename)
                    if len(file_configuration) > 0:
                        file_configurations[filename.name] = file_configuration

        configuration = cls()
        configuration.__from_directory = directory
        file_configurations = [
            file_configurations[filename]
            for filename in reversed(known_configuration_filenames)
            if filename in file_configurations
        ]
        for file_configuration in file_configurations:
            if file_configuration is not None:
                configuration.update(file_configuration)

        return configuration

    def __getitem__(self, key: str) -> Any:
        return self.__configuration[key]

    def __setitem__(self, key: str, value: Any):
        if self.start_with_placeholders and key not in self.__configuration:
            raise KeyError(f'"{self.name}" table does not contain "{key}"')
        desired_type = self.fields[key]
        if (
            hasattr(desired_type, "__origin__")
            and desired_type.__origin__.__name__ == "Union"
        ):
            values = []
            errors = []
            for optional_type in desired_type.__args__:
                try:
                    values.append(typepigeon.to_type(value, optional_type))
                except Exception as error:
                    errors.append(error)
            if len(values) == 0:
                raise RuntimeError(";".join(errors))
            elif len(values) > 1:
                warnings.warn(
                    f'multiple possible options for parsing "{value}"; {values}'
                )
            self.__configuration[key] = values[0]
        else:
            self.__configuration[key] = typepigeon.to_type(value, desired_type)

    def update(self, items: Mapping):
        for key, value in items.items():
            if value is not None and (not hasattr(value, "__len__") or len(value) > 0):
                self[key] = value

    def __delitem__(self, key: str):
        raise RuntimeError("cannot delete configuration entry; set as `None` instead")

    def __iter__(self) -> Iterator:
        yield from self.__configuration

    def __len__(self) -> int:
        lengths = {
            key: len(entry) if hasattr(entry, "__len__") else 1
            for key, entry in self.__configuration.items()
            if entry is not None
        }
        return len([length for length in lengths.values() if length > 0])

    def to_toml(self) -> str:
        def table_to_toml(table_name: str, table: Mapping[str, Any]) -> str:
            base_table_string = f"[{table_name}]\n"
            sub_table_strings = []
            for key, value in table.items():
                if value is None:
                    continue
                elif not isinstance(value, Mapping):
                    base_table_string += f"{key} = {repr(value)}\n"
                else:
                    sub_table_strings.append(table_to_toml(table_name=key, table=value))
            return base_table_string + "\n" + "\n".join(sub_table_strings)

        return table_to_toml(table_name=self.name, table=self.__configuration)

    def __repr__(self) -> str:
        configuration_string = ", ".join(
            f"{key}={repr(value)}"
            for key, value in self.__configuration.items()
            if value is not None and (not hasattr(value, "__len__") or len(value) > 0)
        )
        return f"{self.__class__.__name__}({configuration_string})"


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
                if isinstance(value, str):
                    if value in filenames:
                        value = {"file": value}
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
                            value = {"file": license_files[0]}
                        else:
                            value = None
            elif key == "readme":
                if isinstance(value, str):
                    if value not in filenames:
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
                            value = {"text": value}
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
                        value[entry_point_location] = dict(entry_points)

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


class ToolConfiguration(ConfigurationTable, ABC):
    """
    abstraction of an individual tool configuration
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.name.startswith("tool."):
            raise ValueError(f'"{self.name}" must start with `tool.`')


class SetuptoolsConfiguration(ToolConfiguration):
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


class ToolTable(ConfigurationTable):
    """
    abstraction of the top-level ``[tool]`` table in ``pyproject.toml``
    """

    name = "tool"
    fields = {
        "setuptools": SetuptoolsConfiguration,
        "setuptools_scm": None,
        "pytest": None,
        "coverage": None,
        "ruff": None,
    }
    start_with_placeholders = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for table_name, table in self.fields.items():
            if table is not None:
                self._ConfigurationTable__configuration[table_name] = table()

    def __setitem__(self, table_name: str, table: "ToolConfiguration"):
        if (
            table_name in self.fields
            and self.fields[table_name] is not None
            and table is not None
        ):
            configuration = self.fields[table_name]()
            configuration.update(table)
            table = configuration
        super().__setitem__(key=table_name, value=table)

    def __len__(self) -> int:
        return len(self._ConfigurationTable__configuration)
