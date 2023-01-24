from abc import ABC
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Collection, Iterator, Mapping, MutableMapping, Union

import tomli
import tomli_w
import typepigeon
from ini2toml.api import Translator

from peppyproject.files import SETUP_CFG, inify, inify_mapping, read_setup_py


class ConfigurationTable(MutableMapping, ABC):
    """
    abstraction of a TOML configuration table
    """

    name: str
    fields: dict[str, Any]
    start_with_placeholders: bool = True

    def __init__(self, **kwargs):
        if self.start_with_placeholders:
            self.__configuration = {key: None for key in self.fields}
        else:
            self.__configuration = {}
        if len(kwargs) > 0:
            self.update(kwargs)

    @classmethod
    def from_file(cls, filename: str) -> "ConfigurationTable":
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
        elif (
            filename.suffix.lower() in [".cfg", ".ini"]
            or filename.name.lower() == "setup.py"
        ):
            if filename.suffix.lower() in [".cfg", ".ini"]:
                with open(filename) as configuration_file:
                    ini_string = configuration_file.read()
                profile_name = filename.name.lower()
                setup_py = None
            else:
                setup_py = read_setup_py(filename)
                setup_cfg = ConfigParser()
                for section_name, section in SETUP_CFG.items():
                    if section != "DEFAULT":
                        for key, value in setup_py.items():
                            if key.strip() in section:
                                if not isinstance(value, Mapping):
                                    value = inify(value=value)
                                    if section_name not in setup_cfg.sections():
                                        setup_cfg.add_section(section_name)
                                    setup_cfg.set(section_name, key, value)
                                else:
                                    value = inify_mapping(
                                        mapping=value, name=f"{section_name}.{key}"
                                    )
                                    for (
                                        value_section_name,
                                        value_section,
                                    ) in value.items():
                                        if len(value_section) == 0:
                                            if (
                                                value_section_name
                                                == "options.packages.find"
                                            ):
                                                value_section["namespaces"] = "False"
                                            else:
                                                continue
                                        if (
                                            value_section_name
                                            not in setup_cfg.sections()
                                        ):
                                            setup_cfg.add_section(value_section_name)
                                        for (
                                            entry_name,
                                            entry,
                                        ) in value_section.items():
                                            setup_cfg.set(
                                                value_section_name,
                                                entry_name,
                                                entry,
                                            )
                with NamedTemporaryFile() as temporary_file:
                    with open(temporary_file.name, "w") as setup_cfg_file:
                        setup_cfg.write(setup_cfg_file)
                    with open(temporary_file.name) as setup_cfg_file:
                        ini_string = setup_cfg_file.read()
                profile_name = "setup.cfg"
            toml_string = Translator().translate(
                ini_string,
                profile_name=profile_name,
            )
            file_configuration = tomli.loads(toml_string)
            if "project" in file_configuration:
                project_table = file_configuration["project"]
                if "homepage" in project_table:
                    if "urls" not in project_table:
                        project_table["urls"] = ConfigurationSubTable()
                    project_table["urls"]["homepage"] = project_table["homepage"]
                    del project_table["homepage"]
                file_configuration["project"] = project_table
            if "tool" in file_configuration:
                tool_table = file_configuration["tool"]
                if "setuptools" in tool_table:
                    setuptools_table = tool_table["setuptools"]
                    if "packages" in setuptools_table:
                        packages_table = setuptools_table["packages"]
                        if "find" in packages_table:
                            if "namespaces" in packages_table["find"]:
                                packages_table["find"]["namespaces"] = (
                                    packages_table["find"]["namespaces"] == "True"
                                )
                        setuptools_table["packages"] = packages_table
                    if setup_py is not None:
                        if "extras-require" in setuptools_table:
                            if "project" not in file_configuration:
                                file_configuration["project"] = ConfigurationSubTable()
                            file_configuration["project"][
                                "optional-dependencies"
                            ] = setup_py["extras_require"]
                            del setuptools_table["extras-require"]
                        if "package-data" in setuptools_table:
                            if "project" not in file_configuration:
                                setuptools_table = ConfigurationSubTable()
                            setuptools_table["package-data"] = setup_py["package_data"]
                    tool_table["setuptools"] = setuptools_table
                file_configuration["tool"] = tool_table
            base_table = cls.name.split(".", 1)[0]
            if base_table in file_configuration:
                configuration.update(file_configuration[base_table])

        return configuration

    @classmethod
    def from_directory(cls, directory: str) -> "ConfigurationTable":
        if not isinstance(directory, Path):
            directory = Path(directory)

        known_filenames = ["pyproject.toml", "setup.cfg", "setup.py"]
        known_suffixes = [".cfg", ".ini"]

        file_configurations = {}
        for filename in directory.iterdir():
            if filename.is_file() and (
                filename.name.lower() in known_filenames
                or filename.suffix.lower() in known_suffixes
            ):
                file_configuration = cls.from_file(filename)
                if len(file_configuration) > 0:
                    file_configurations[filename.name] = file_configuration

        configuration = cls()
        configuration.__from_directory = directory
        file_configurations = [
            file_configurations[filename]
            for filename in reversed(known_filenames)
            if filename in file_configurations
        ]
        for file_configuration in file_configurations:
            if file_configuration is not None and len(file_configuration) > 0:
                configuration.update(file_configuration)

        return configuration

    def __getitem__(self, key: str) -> Any:
        return self.__configuration[key]

    def __setitem__(self, key: str, value: Any):
        if key in self.fields:
            desired_type = self.fields[key]
            subtable_class = (
                desired_type
                if desired_type is not None and not isinstance(desired_type, Mapping)
                else ConfigurationSubTable
            )
            if hasattr(desired_type, "__origin__") and (
                (
                    hasattr(desired_type.__origin__, "__name__")
                    and desired_type.__origin__.__name__ == "Union"
                )
                or (
                    hasattr(desired_type.__origin__, "_name")
                    and desired_type.__origin__._name == "Union"
                )
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
                                    sub_value,
                                    desired_type[sub_key],
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
            ],
        )

    @property
    def __toml(self) -> dict[str, Union[str, dict]]:
        return {
            key: value.__toml
            if isinstance(value, ConfigurationTable)
            else str(value)
            if not isinstance(
                value,
                (str, int, float, bool, datetime, Collection, Mapping),
            )
            else value
            for key, value in self.__configuration.items()
            if value is not None
        }

    @property
    def configuration(self) -> str:
        return tomli_w.dumps(to_dict({self.name: self.__toml}))

    def to_file(self, filename: str):
        with open(filename, "w") as configuration_file:
            configuration_file.write(self.configuration)

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


def to_dict(value: Mapping) -> dict:
    output = {}
    if isinstance(value, Mapping):
        for entry_name, entry in value.items():
            if isinstance(entry, Mapping):
                entry = {
                    subentry_name: to_dict(subentry)
                    for subentry_name, subentry in entry.items()
                }
            output[entry_name] = entry
    else:
        output = value
    return output
