from pathlib import Path

import pytest
import tomli
from typer.testing import CliRunner

from peppyproject.__main__ import app

TEST_DIRECTORY = Path(__file__).parent / "data"

runner = CliRunner()


@pytest.mark.parametrize("directory", ["pyproject_toml", "setup_cfg", "setup_py"])
@pytest.mark.parametrize("output", [None, "pyproject.toml"])
def test_write(directory, output, tmp_path):
    input_path = TEST_DIRECTORY / "input" / directory
    test_path = tmp_path / output if output is not None else None
    reference_path = TEST_DIRECTORY / "reference" / directory / "pyproject.toml"

    arguments = [str(input_path)]
    if test_path is not None:
        arguments.extend(["-o", str(test_path)])
    result = runner.invoke(app, arguments)

    assert result.exit_code == 0

    with open(reference_path, "rb") as reference_file:
        reference_tomli = tomli.load(reference_file)

    if test_path is None:
        assert tomli.loads(result.stdout) == reference_tomli
    else:
        with open(test_path, "rb") as test_file:
            assert tomli.load(test_file) == reference_tomli
