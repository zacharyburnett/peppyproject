from pathlib import Path

import typer

from peppyproject import PyProjectConfiguration


def peppyproject_command(directory: Path = None, output: Path = None):
    if directory is None:
        directory = Path.cwd()

    configuration = PyProjectConfiguration.from_directory(directory=directory)
    toml_string = configuration.to_toml()
    if output is None:
        print(toml_string)
    else:
        with open(output, 'w') as toml_file:
            toml_file.write(toml_string)


def main():
    typer.run(peppyproject_command)


if __name__ == "__main__":
    main()
