from pathlib import Path

import pytest
import tomli

from peppyproject.configuration import PyProjectConfiguration

TEST_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize("directory", ["pyproject_toml", "setup_cfg", "setup_py"])
def test_to_toml(directory):
    configuration = PyProjectConfiguration.from_directory(
        TEST_DIRECTORY / "input" / directory,
    )

    toml_string = configuration.toml

    with open(
        TEST_DIRECTORY / "reference" / directory / "pyproject.toml",
        "rb",
    ) as toml_file:
        assert tomli.loads(toml_string) == tomli.load(toml_file)
