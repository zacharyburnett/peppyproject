from pathlib import Path

import typer

from peppyproject import PyProjectConfiguration

app = typer.Typer(add_completion=False)


@app.command()
def main(
    directory: Path = typer.Argument(
        None, help="directory from which to read configuration"
    ),
    output_filename: Path = typer.Option(
        None, "-o", "--output", help="path to which to write TOML"
    ),
):
    """
    read a Python project configuration and output a PEP621-compliant `pyproject.toml`
    """

    if directory is None:
        directory = Path.cwd()

    configuration = PyProjectConfiguration.from_directory(directory=directory)
    toml_string = configuration.configuration
    if output_filename is None:
        print(toml_string)
    else:
        if not output_filename.parent.exists():
            output_filename.mkdir(parents=True, exist_ok=True)
        with open(output_filename, "w") as toml_file:
            toml_file.write(toml_string)


if __name__ == "__main__":
    app()
