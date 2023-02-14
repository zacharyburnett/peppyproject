# `peppyproject`

[![build](https://github.com/zacharyburnett/peppyproject/actions/workflows/build.yml/badge.svg)](https://github.com/zacharyburnett/peppyproject/actions/workflows/build.yml)
[![pypi](https://img.shields.io/pypi/v/peppyproject)](https://pypi.org/project/peppyproject)
[![implementation](https://img.shields.io/pypi/implementation/peppyproject)](https://pypi.org/project/peppyproject)
[![python](https://img.shields.io/pypi/pyversions/peppyproject)](https://pypi.org/project/peppyproject)
[![tests](https://github.com/zacharyburnett/peppyproject/actions/workflows/tests.yml/badge.svg)](https://github.com/zacharyburnett/peppyproject/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/zacharyburnett/peppyproject/branch/main/graph/badge.svg?token=AJ6SZMOP2N)](https://codecov.io/github/zacharyburnett/peppyproject)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

`peppyproject` creates a PEP621-compliant `pyproject.toml` file from an existing Python project's build
configuration (`setup.cfg`, `setup.py`, `tox.ini`, `pytest.ini`, etc.).

### Installation

```shell
pip install peppyproject
```

### Usage

```
Usage: peppyproject [OPTIONS] [DIRECTORY]

  read a Python project configuration and output a PEP621-compliant `pyproject.toml`

Arguments:
  [DIRECTORY]  directory from which to read configuration

Options:
  -o, --output PATH  path to which to write TOML
  --help             Show this message and exit.
```

### API

`peppyproject` uses `ini2toml[full]` to read `setup.cfg` and INI files, and `ast.literal_eval()` to read and parse
a `setup.py` file. It assumes you have vetted the ``setup.py`` and does not perform any sanitization or safety checking;
thus, it is inadvisable to use on unknown or potentially malicious ``setup.py`` scripts.

```python
from peppyproject import PyProjectConfiguration

configuration = PyProjectConfiguration.from_directory('./my_python_project')
configuration.to_file('./my_python_project/pyproject.toml')
```