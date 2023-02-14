from pathlib import Path

import pytest
import tomli

from peppyproject.configuration import PyProjectConfiguration

TEST_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize("directory", ["pyproject_toml", "setup_cfg", "setup_py"])
def test_to_file(directory, tmp_path):
    input_path = TEST_DIRECTORY / "input" / directory
    test_path = tmp_path / "pyproject.toml"
    reference_path = TEST_DIRECTORY / "reference" / directory / "pyproject.toml"

    configuration = PyProjectConfiguration.from_directory(input_path)
    configuration.to_file(test_path)

    with open(reference_path, "rb") as reference_file:
        reference_tomli = tomli.load(reference_file)

    with open(test_path, "rb") as test_file:
        assert tomli.load(test_file) == reference_tomli
