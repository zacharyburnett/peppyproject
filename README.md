# `peppyproject`

[![pypi](https://img.shields.io/pypi/v/peppyproject)](https://pypi.org/project/peppyproject)
[![implementation](https://img.shields.io/pypi/implementation/peppyproject)](https://pypi.org/project/peppyproject)
[![python](https://img.shields.io/pypi/pyversions/peppyproject)](https://pypi.org/project/peppyproject)
[![tests](https://github.com/zacharyburnett/peppyproject/actions/workflows/tests.yml/badge.svg)](https://github.com/zacharyburnett/peppyproject/actions/workflows/tests.yml)
[![build](https://github.com/zacharyburnett/peppyproject/actions/workflows/build.yml/badge.svg)](https://github.com/zacharyburnett/peppyproject/actions/workflows/build.yml)

`peppyproject` creates a PEP621-compliant `pyproject.toml` file from an existing Python project's build
configuration (`setup.cfg`, `setup.py`, `tox.ini`, etc.).

```commandline
pip install peppyproject
peppyproject --input ./my_python_project --output new-pyproject.toml
```

`peppyproject` uses `ini2toml[full]` to read `setup.cfg` and INI files, and `ast.literal_eval()` to read and parse
a `setup.py` file.