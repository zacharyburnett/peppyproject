from pathlib import Path

import typer

from peppyproject import PyProjectConfiguration


def peppyproject_command(input: Path = None, output: Path = None):
    if input is None:
        input = Path.cwd()

    configuration = PyProjectConfiguration.from_directory(directory=input)
    toml_string = configuration.configuration()
    if output is None:
        print(toml_string)
    else:
        if not output.parent.exists():
            output.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as toml_file:
            toml_file.write(toml_string)


def main():
    typer.run(peppyproject_command)
