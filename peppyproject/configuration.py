from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from typing import List, Dict, Union, Any, Mapping

import tomli as tomli
import typepigeon as typepigeon

PEP621 = {
    'name': str,
    'version': str,
    'description': str,
    'readme': Union[str, Dict[str, str]],
    'requires-python': str,
    'license': Dict[str, str],
    'authors': List[Dict[str, str]],
    'keywords': List[str],
    'classifiers': List[str],
    'urls': Dict[str, str],
    'scripts': Dict[str, str],
    'gui-scripts': Dict[str, str],
    'entry-points': Dict[str, Dict[str, str]],
    'dependencies': List[str],
    'optional-dependencies': Dict[str, List[str]],
    'dynamic': List[str],
}


class ProjectConfiguration:
    """
    PEP621 configuration metadata
    """

    def __init__(self):
        self.__configuration = {
            'project': {key: {} for key in PEP621},
            'tool': {},
        }

    @classmethod
    def from_file(cls, filename: PathLike) -> 'ProjectConfiguration':
        if not isinstance(filename, Path):
            filename = Path(filename)

        configuration = cls()
        if filename.name.lower() == 'pyproject.toml':
            with open(filename, 'rb') as configuration_file:
                configuration.update(tomli.load(configuration_file))
        elif filename.name.lower() == 'setup.cfg':
            parser = ConfigParser()
            parser.read([filename])
            dict(parser.items('metadata'))
        elif filename.name.lower() == 'setup.py':
            with open(filename) as configuration_file:
                pass

        return

    def __getitem__(self, key: str) -> Any:
        pass

    def __setitem__(self, key: str, value: Any):
        pass

    def update(self, items: Mapping):
        for table_name, table in items:
            if table_name == 'project':
                for key, value in table.items():
                    self[key] = typepigeon.convert_value(value, PEP621[key])
