import warnings
from abc import ABC
from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, MutableMapping

import tomli
import tomli_w
import typepigeon

from peppyproject.files import SETUP_CFG, read_setup_py


class ConfigurationTable(MutableMapping, ABC):
    """
    abstraction of a TOML configuration table
    """

    name: str
    fields: Dict[str, Any]
    start_with_placeholders: bool = True
    inline_tables: List[str] = []

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
                    if section_translations is not None:
                        for key, value in setup_cfg.items(section):
                            if key in section_translations:
                                table, entry = section_translations[key].rsplit(".", 1)
                                if table == cls.name:
                                    value = [
                                        line
                                        for line in value.splitlines()
                                        if len(line) > 0
                                    ]
                                    if len(value) == 1:
                                        value = value[0]
                                    configuration[entry] = value
                    elif section != "DEFAULT" and cls.name == "tool":
                        table = (
                            section.replace("tool:", "")
                            if section.startswith("tool:")
                            else section
                        )
                        if ":" in table:
                            table, subtable = table.split(":")
                        else:
                            subtable = None
                        if table not in configuration:
                            if table in configuration.fields:
                                value = configuration.fields[table]
                                if isinstance(value, type):
                                    value = value()
                                configuration[table] = value
                            else:
                                configuration[table] = {}
                        if subtable is not None:
                            if (
                                subtable not in configuration[table]
                                or configuration[table][subtable] is None
                            ):
                                subtable_class = (
                                    configuration.fields[subtable]
                                    if subtable in configuration.fields
                                    else ConfigurationSubTable
                                )
                                configuration[table][subtable] = subtable_class()
                            for key, value in setup_cfg.items(section):
                                configuration[table][subtable][key] = value
                        else:
                            for key, value in setup_cfg.items(section):
                                configuration[table][key] = value
                else:
                    values = setup_cfg.items(section)
                    if section in ["options.extras_require", "options.entry_points"]:
                        values = dict(values)
                    base_section, key = section.split(".", 1)
                    section_translations = (
                        SETUP_CFG[base_section] if base_section in SETUP_CFG else None
                    )
                    if base_section in SETUP_CFG:
                        if section_translations is not None:
                            if key in section_translations:
                                table, entry = section_translations[key].rsplit(".", 1)
                                if table == cls.name:
                                    configuration[entry] = values
                        elif base_section != "DEFAULT" and cls.name == "tool":
                            if base_section not in configuration:
                                configuration[base_section] = configuration.fields.get(
                                    base_section, {}
                                )
                            for key, value in setup_cfg.items(section):
                                configuration[base_section][key] = value
        elif filename.name.lower() == "setup.py":
            setup_py = read_setup_py(filename)
            for _section, section_translations in SETUP_CFG.items():
                for key, value in setup_py.items():
                    if key in section_translations:
                        table, entry = section_translations[key].rsplit(".", 1)
                        tables = table.split(".")
                        if tables[0] == cls.name:
                            if len(tables) > 1:
                                subtable = tables[1]
                                if subtable not in configuration:
                                    subtable_class = (
                                        configuration.fields[subtable]
                                        if subtable in configuration.fields
                                        else ConfigurationSubTable
                                    )
                                    configuration[subtable] = subtable_class()
                                configuration[subtable][entry] = value
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
            if filename.is_file() and filename.name in known_configuration_filenames:
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
            message = f'"{self.name}" table does not contain "{key}"'
            raise KeyError(message)

        if key in self.fields:
            desired_type = self.fields[key]
            subtable_class = (
                desired_type
                if desired_type is not None and not isinstance(desired_type, Mapping)
                else ConfigurationSubTable
            )
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
                if len(values) > 1:
                    warnings.warn(
                        f'multiple possible options for parsing "{value}"; {values}'
                    )
                self.__configuration[key] = values[0]
            else:
                if isinstance(desired_type, Mapping) and isinstance(value, Mapping):
                    if len(value) > 0:
                        for sub_key, sub_value in value.items():
                            if sub_key in desired_type:
                                if (
                                    key not in self.__configuration
                                    or self.__configuration[key] is None
                                ):
                                    self.__configuration[key] = subtable_class()
                                self[key][sub_key] = typepigeon.to_type(
                                    sub_value, desired_type[sub_key]
                                )
                    else:
                        self.__configuration[key] = subtable_class()
                else:
                    self.__configuration[key] = typepigeon.to_type(value, desired_type)
        else:
            self.__configuration[key] = value

    def update(self, items: Mapping):
        for key, value in items.items():
            if value is not None and (not hasattr(value, "__len__") or len(value) > 0):
                self[key] = value

    def __delitem__(self, key: str):
        message = "cannot delete configuration entry; set as `None` instead"
        raise RuntimeError(message)

    def __iter__(self) -> Iterator:
        yield from self.__configuration

    def __len__(self) -> int:
        lengths = {
            key: len(entry) if hasattr(entry, "__len__") else 1
            for key, entry in self.__configuration.items()
            if entry is not None
        }
        return len(
            [
                length
                for length in lengths.values()
                if not self.start_with_placeholders or length > 0
            ]
        )

    def to_toml(self) -> str:
        return table_to_toml(table_name=self.name, table=self.__configuration)

    def __repr__(self) -> str:
        configuration_string = {
            key: value
            for key, value in self.__configuration.items()
            if value is not None
            and (
                not self.start_with_placeholders
                or (not hasattr(value, "__len__") or len(value) > 0)
            )
        }
        return repr(configuration_string)


class ConfigurationSubTable(ConfigurationTable):
    name = None
    fields = {}
    start_with_placeholders = False


def table_to_toml(table_name: str, table: MutableMapping[str, Any]) -> str:
    table = {
        table_name: {key: value for key, value in table.items() if value is not None}
    }
    return tomli_w.dumps(table)
