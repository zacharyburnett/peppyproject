# https://setuptools.pypa.io/en/latest/userguide/declarative_config.html#compatibility-with-other-tools
import ast
import contextlib
import re
import warnings
from pathlib import Path
from typing import Any, Collection, Mapping, Union

SETUP_CFG_INDENT = " " * 4
SETUP_CFG = {
    "metadata": {
        "name": "project.name",
        "version": "project.version",
        "author": "project.authors",
        "description": "project.description",
        "long_description": "project.readme",
        "keywords": "project.keywords",
        "license": "project.license",
        "classifiers": "project.classifiers",
    },
    "options": {
        "zip_safe": "tool.setuptools.zip-safe",
        "include_package_data": "tool.setuptools.include-package-data",
        "packages": "tool.setuptools.packages",
        "install_requires": "project.dependencies",
        "setup_requires": "build-system.requires",
        "package_data": "tool.setuptools.package-data",
        "package_dir": "tool.setuptools.package-dir",
        "entry_points": "project.entry-points",
        "extras_require": "project.optional-dependencies",
    },
}

PYTHON_LINE = {
    "continuing": ["\\", ",", "(", "{", "[", ":"],
    "ending": [")", "}", "]"],
}


def python_statement(
    lines: list[str],
    index: int = 0,
    current_statement: str = None,
    statements: list[str] = None,
) -> tuple[list[str], int]:
    if current_statement is None:
        current_statement = ""

    if statements is None:
        statements = []

    # read line
    line = lines[index]

    # remove comments; TODO: handle `#` in strings / comment
    line = line.rsplit("#", 1)[0].strip()

    # increment line index
    index += 1

    # check if line continues
    if any(
        line.endswith(continuing_character)
        for continuing_character in PYTHON_LINE["continuing"]
    ):
        statements, index = python_statement(
            lines=lines,
            index=index,
            current_statement=current_statement,
            statements=statements,
        )
        current_statement += line.rstrip("\\")
        if len(current_statement) > 0:
            current_statement += " "
        current_statement += statements.pop()
    elif len(line) == 0:
        pass
    else:
        current_statement += line

    if any(
        line.endswith(ending_character) for ending_character in PYTHON_LINE["ending"]
    ) and any(
        statements[-1].endswith(continuing_character)
        for continuing_character in PYTHON_LINE["continuing"]
    ):
        statements[-1] += current_statement
    else:
        statements.extend(current_statement.split(";"))

    return statements, index


def parse_function_parameters(
    parameter_string: str,
    variables: dict[str, Any] = None,
) -> dict[str, Any]:
    if variables is None:
        variables = {}

    function_parameters = {}

    parameters = re.findall(r"(.+?=[^=]+),", parameter_string)
    keyword_arguments = re.findall(r"\*\*\w+", parameter_string)
    parameter_index = 0
    while parameter_index < len(parameters):
        parameter = parameters[parameter_index].strip()
        if parameter.startswith('"') or parameter.startswith("'"):
            parameters[parameter_index - 1] += parameters.pop(parameter_index)
        else:
            parameter_index += 1
    for parameter in parameters:
        name, value = parameter.strip().split("=", 1)
        name = name.strip()
        value = value.strip()
        if "open(" in value:
            value = re.findall(r"open\((.+?)\).read\(\)", value)[0]

        for variable in variables:
            if variable in value:
                value = value.replace(variable, repr(variables[variable]))

        value = re.sub(r"\]\s*\+\s*\[", ",", value)
        value = re.sub(r"\}\s*\+\s*\*\*\{", ",", value)

        try:
            value = ast.literal_eval(value)
        except:
            if name == "version":
                continue

        if isinstance(value, str) and "find_packages(" in value:
            value = {
                "find": parse_function_parameters(
                    parameter_string=value.split("find_packages(", 1)[-1].rsplit(
                        ")",
                        1,
                    )[0],
                    variables=variables,
                ),
            }

        function_parameters[name] = value
    for value in keyword_arguments:
        value = value.replace("**", "")

        for variable in variables:
            if variable in value:
                value = value.replace(variable, repr(variables[variable]))

        value = re.sub(r"\]\s*\+\s*\[", ",", value)
        value = re.sub(r"\}\s*\+\s*\*\*\{", ",", value)

        with contextlib.suppress(Exception):
            value = ast.literal_eval(value)

        for key, entry in value.items():
            function_parameters[key] = entry

    return function_parameters


def read_python_file(filename: str) -> list[str]:
    if not isinstance(filename, Path):
        filename = Path(filename)

    with open(filename) as script_file:
        lines = script_file.readlines()

    statements = []
    index = 0
    while index < len(lines):
        statements, index = python_statement(
            lines=lines,
            index=index,
            statements=statements,
        )

    statements = [statement for statement in statements if len(statement) > 0]

    indices = []
    for index in reversed(range(len(statements))):
        statement = statements[index]
        if any(
            statement.strip().endswith(continuing_character)
            for continuing_character in PYTHON_LINE["continuing"]
        ):
            if index < len(statements) - 1:
                statements[index] += statements[index + 1]
                indices.append(index + 1)
        elif any(
            statement.strip().startswith(ending_character)
            for ending_character in PYTHON_LINE["ending"]
        ):
            statements[index - 1] += statement
            indices.append(index)

    for index in indices:
        statements.pop(index)

    return statements


def read_setup_py(filename: str) -> dict[str, Any]:
    statements = read_python_file(filename)

    setup_parameters = {}
    setup_calls = {
        index: statement
        for index, statement in enumerate(statements)
        if "setup(" in statement
    }

    if len(setup_calls) > 0:
        if len(setup_calls) > 1:
            warnings.warn(f"multiple setup calls found; {setup_calls}")
        setup_call_index, setup_call = next(reversed(setup_calls.items()))

        statements.pop(setup_call_index)

        variables = {}
        for statement in statements:
            if "=" in statement:
                name, value = statement.strip().split("=", 1)
                for variable in variables:
                    if variable in value:
                        value = value.replace(variable, repr(variables[variable]))
                for glob_pattern in re.findall("glob.glob\\((.+)\\)", value):
                    value = value.replace(f"glob.glob({glob_pattern})", glob_pattern)
                with contextlib.suppress(Exception):
                    value = ast.literal_eval(value.strip())
                variables[name.strip()] = value

        setup_parameters = parse_function_parameters(
            parameter_string=setup_call.split("setup(", 1)[-1].rsplit(")", 1)[0],
            variables=variables,
        )

    for parameter in list(setup_parameters):
        value = setup_parameters[parameter]
        if isinstance(value, Mapping) and any(key == "" for key in value):
            setup_parameters[parameter] = {
                key if key != "" else "*": entry for key, entry in value.items()
            }

    return setup_parameters


def inify(value: Any, indent: str = None) -> str:
    if indent is None:
        indent = SETUP_CFG_INDENT
    if isinstance(value, Mapping):
        value = "\n" + "\n".join(
            f'{key}{":" if "find" in value else " ="} {inify(value=entry, indent=indent)}'
            for key, entry in value.items()
        )
    elif isinstance(value, Collection) and not isinstance(value, str):
        value = "\n" + "\n".join(f"{indent}{entry}" for entry in value)
    else:
        value = str(value)

    return value


def inify_mapping(
    mapping: Mapping[str, Any], name: str, level: int = 0
) -> dict[str, Union[str, dict[str, str]]]:
    output = {name: {}}
    for key, value in mapping.items():
        if not isinstance(value, Mapping):
            output[name][key] = inify(value)
        else:
            output.update(inify_mapping(value, name=f"{name}.{key}", level=level + 1))
    return {key: inify(value) if level > 1 else value for key, value in output.items()}
