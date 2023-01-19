from pathlib import Path

import pytest
import tomli

from peppyproject.configuration import PyProjectConfiguration

TEST_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize("directory", ["pyproject_toml", "setup_cfg", "setup_py"])
def test_to_file(directory):
    configuration = PyProjectConfiguration.from_directory(
        TEST_DIRECTORY / "input" / directory,
    )

    configuration_string = configuration.configuration

    with open(
        TEST_DIRECTORY / "reference" / directory / "pyproject.toml",
        "rb",
    ) as configuration_file:
        assert tomli.loads(configuration_string) == tomli.load(configuration_file)
