from pathlib import Path

import pytest
import tomli

from peppyproject.configuration import PyProjectConfiguration

TEST_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize("package", ["romancal", "jwst", "crds"])
def test_to_toml(package):
    configuration = PyProjectConfiguration.from_directory(
        TEST_DIRECTORY / "input" / package
    )

    toml_string = configuration.to_toml()

    with open(
        TEST_DIRECTORY / "reference" / package / "pyproject.toml", "rb"
    ) as toml_file:
        assert tomli.loads(toml_string) == tomli.load(toml_file)
