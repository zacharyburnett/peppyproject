from pathlib import Path

import typer

from peppyproject import PyProjectConfiguration


def peppyproject_command(
    input_directory: Path = typer.Argument(
        None, help="directory from which to read configuration"
    ),
    output_filename: Path = typer.Option(
        None, "-o", "--output", help="path to which to write TOML"
    ),
):
    """
    read a Python project configuration and output a PEP621-compliant `pyproject.toml`
    """

    if input_directory is None:
        input_directory = Path.cwd()

    configuration = PyProjectConfiguration.from_directory(directory=input_directory)
    toml_string = configuration.configuration
    if output_filename is None:
        print(toml_string)
    else:
        if not output_filename.parent.exists():
            output_filename.mkdir(parents=True, exist_ok=True)
        with open(output_filename, "w") as toml_file:
            toml_file.write(toml_string)


def main():
    typer.run(peppyproject_command)
