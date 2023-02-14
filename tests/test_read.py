from pathlib import Path

from peppyproject.files import read_python_file, read_setup_py

TEST_DIRECTORY = Path(__file__).parent / "data"


def test_read_python_file():
    statements = read_python_file(TEST_DIRECTORY / "input" / "setup_py" / "setup.py")
    assert statements == [
        "import sys",
        "import glob",
        "from distutils.core import setup",
        "import setuptools",
        'STD_MISSION_FILES = [ "*.dat", "*.yaml", "*.json", "tpns/*.tpn", "tpns/includes/*.tpn", "specs/*.spec", '
        '"specs/*.rmap", "specs/*.json", ]',
        'setup_pars = { "packages": [ "crds", "crds.bestrefs", "crds.certify", "crds.certify.validators", '
        '"crds.client", "crds.core", "crds.io", "crds.submit", "crds.misc", "crds.misc.synphot", "crds.refactoring", '
        '"crds.hst", "crds.jwst", "crds.tobs", "crds.roman", "crds.tests", ], "package_dir": { "crds": "crds", '
        '"crds.bestrefs": "crds/bestrefs", "crds.certify": "crds/certify", "crds.certify.validators": '
        '"crds/certify/validators", "crds.client": "crds/client", "crds.core": "crds/core", "crds.io": "crds/io", '
        '"crds.submit": "crds/submit", "crds.misc": "crds/misc", "crds.misc.synphot": "crds/misc/synphot", '
        '"crds.refactoring": "crds/refactoring", "crds.hst": "crds/hst", "crds.jwst": "crds/jwst", "crds.roman": '
        '"crds/roman", "crds.tobs": "crds/tobs", "crds.tests": "crds/tests", }, "package_data": { "crds.hst": '
        'STD_MISSION_FILES, "crds.jwst": STD_MISSION_FILES, "crds.roman": STD_MISSION_FILES, "crds.tobs": '
        'STD_MISSION_FILES, }, "scripts": glob.glob("scripts/*"), }',
        'TEST_DEPS = [ "lockfile", "mock", "nose", "pytest", "pylint", "flake8", "bandit", ]',
        'SUBMISSION_DEPS = ["requests", "lxml", "parsley"]',
        'setup( name="crds", provides=["crds"], use_scm_version={"write_to": "crds/_version.py"}, '
        'description="Calibration Reference Data System,  HST/JWST/Roman reference file management", '
        'long_description=open("README.rst").read(), author="STScI CRDS s/w developers", '
        'url="https://hst-crds.stsci.edu", license="BSD", python_requires=">=3.8", setup_requires=["setuptools_scm"], '
        'install_requires=["astropy", "numpy", "filelock", "asdf"] + SUBMISSION_DEPS, extras_require={ "jwst": '
        '["jwst"], "roman": ["roman_datamodels"], "submission": ["requests", "lxml", "parsley"], "dev": ["ipython", '
        '"jupyterlab", "ansible", "helm", "nose-cprof", "coverage"], "test": TEST_DEPS, "docs": [ "sphinx", '
        '"sphinx_rtd_theme", "docutils", "sphinx_automodapi", "sphinx-tabs", ], "aws": ["boto3", "awscli"], "synphot": '
        '["stsynphot", "pysynphot"], }, tests_require=TEST_DEPS, zip_safe=False, classifiers=[ "Intended Audience :: '
        'Science/Research", "License :: OSI Approved :: BSD License", "Operating System :: POSIX :: Linux", '
        '"Operating System :: MacOS :: MacOS X", "Programming Language :: Python :: 3", "Topic :: '
        'Scientific/Engineering :: Astronomy", ], project_urls={ "Documentation": '
        '"https://hst-crds.stsci.edu/static/users_guide/index.html", "Bug Reports": '
        '"https://github.com/spacetelescope/crds/issues/", "Source": "https://github.com/spacetelescope/crds/", '
        '"Help": "https://hsthelp.stsci.edu/", }, **setup_pars)',
    ]


def test_read_setup_py():
    setup_parameters = read_setup_py(TEST_DIRECTORY / "input" / "setup_py" / "setup.py")
    assert setup_parameters == {
        "name": "crds",
        "provides": ["crds"],
        "use_scm_version": {"write_to": "crds/_version.py"},
        "description": "Calibration Reference Data System,  HST/JWST/Roman reference file management",
        "long_description": "README.rst",
        "author": "STScI CRDS s/w developers",
        "url": "https://hst-crds.stsci.edu",
        "license": "BSD",
        "python_requires": ">=3.8",
        "setup_requires": ["setuptools_scm"],
        "install_requires": [
            "astropy",
            "numpy",
            "filelock",
            "asdf",
            "requests",
            "lxml",
            "parsley",
        ],
        "extras_require": {
            "jwst": ["jwst"],
            "roman": ["roman_datamodels"],
            "submission": ["requests", "lxml", "parsley"],
            "dev": [
                "ipython",
                "jupyterlab",
                "ansible",
                "helm",
                "nose-cprof",
                "coverage",
            ],
            "test": [
                "lockfile",
                "mock",
                "nose",
                "pytest",
                "pylint",
                "flake8",
                "bandit",
            ],
            "docs": [
                "sphinx",
                "sphinx_rtd_theme",
                "docutils",
                "sphinx_automodapi",
                "sphinx-tabs",
            ],
            "aws": ["boto3", "awscli"],
            "synphot": ["stsynphot", "pysynphot"],
        },
        "tests_require": [
            "lockfile",
            "mock",
            "nose",
            "pytest",
            "pylint",
            "flake8",
            "bandit",
        ],
        "zip_safe": False,
        "classifiers": [
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS :: MacOS X",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering :: Astronomy",
        ],
        "project_urls": {
            "Documentation": "https://hst-crds.stsci.edu/static/users_guide/index.html",
            "Bug Reports": "https://github.com/spacetelescope/crds/issues/",
            "Source": "https://github.com/spacetelescope/crds/",
            "Help": "https://hsthelp.stsci.edu/",
        },
        "packages": [
            "crds",
            "crds.bestrefs",
            "crds.certify",
            "crds.certify.validators",
            "crds.client",
            "crds.core",
            "crds.io",
            "crds.submit",
            "crds.misc",
            "crds.misc.synphot",
            "crds.refactoring",
            "crds.hst",
            "crds.jwst",
            "crds.tobs",
            "crds.roman",
            "crds.tests",
        ],
        "package_dir": {
            "crds": "crds",
            "crds.bestrefs": "crds/bestrefs",
            "crds.certify": "crds/certify",
            "crds.certify.validators": "crds/certify/validators",
            "crds.client": "crds/client",
            "crds.core": "crds/core",
            "crds.io": "crds/io",
            "crds.submit": "crds/submit",
            "crds.misc": "crds/misc",
            "crds.misc.synphot": "crds/misc/synphot",
            "crds.refactoring": "crds/refactoring",
            "crds.hst": "crds/hst",
            "crds.jwst": "crds/jwst",
            "crds.roman": "crds/roman",
            "crds.tobs": "crds/tobs",
            "crds.tests": "crds/tests",
        },
        "package_data": {
            "crds.hst": [
                "*.dat",
                "*.yaml",
                "*.json",
                "tpns/*.tpn",
                "tpns/includes/*.tpn",
                "specs/*.spec",
                "specs/*.rmap",
                "specs/*.json",
            ],
            "crds.jwst": [
                "*.dat",
                "*.yaml",
                "*.json",
                "tpns/*.tpn",
                "tpns/includes/*.tpn",
                "specs/*.spec",
                "specs/*.rmap",
                "specs/*.json",
            ],
            "crds.roman": [
                "*.dat",
                "*.yaml",
                "*.json",
                "tpns/*.tpn",
                "tpns/includes/*.tpn",
                "specs/*.spec",
                "specs/*.rmap",
                "specs/*.json",
            ],
            "crds.tobs": [
                "*.dat",
                "*.yaml",
                "*.json",
                "tpns/*.tpn",
                "tpns/includes/*.tpn",
                "specs/*.spec",
                "specs/*.rmap",
                "specs/*.json",
            ],
        },
        "scripts": "scripts/*",
    }
