from pathlib import Path

from peppyproject.configuration import PyProjectConfiguration

TEST_DIRECTORY = Path(__file__).parent / "data"


def test_pyproject_configuration_pyproject_toml():
    configuration = PyProjectConfiguration.from_directory(
        TEST_DIRECTORY / "input" / "romancal"
    )

    assert len(configuration["project"]) == 13
    assert len(configuration["build-system"]) == 2
    assert len(configuration['tool']) == 3
    assert len(configuration["tool"]["setuptools"]) == 3

    assert configuration["project"]["name"] == "romancal"
    assert (
            configuration["project"]["description"]
            == "Library for calibration of science observations from the Nancy Grace Roman Space Telescope"
    )
    assert configuration["project"]["readme"] == "README.md"
    assert configuration["project"]["requires-python"] == ">=3.8"
    assert configuration["project"]["license"] == {"file": "LICENSE"}
    assert configuration["project"]["authors"] == [
        {"name": "Roman calibration pipeline developers", "email": "help@stsci.edu"}
    ]
    assert configuration["project"]["classifiers"] == [
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ]
    assert configuration["project"]["urls"] == {
        "tracker": "https://github.com/spacetelescope/romancal/issues",
        "documentation": "https://roman-pipeline.readthedocs.io/en/stable/",
        "repository": "https://github.com/spacetelescope/romancal",
    }
    assert configuration["project"]["scripts"] == {
        "okify_regtests": "romancal.scripts.okify_regtests:main",
        "schema_editor": "romancal.scripts.schema_editor:main",
        "schemadoc": "romancal.scripts.schemadoc:main",
        "verify_install_requires": "romancal.scripts.verify_install_requires:main",
    }
    assert configuration["project"]["entry-points"] == {
        "stpipe.steps": {"romancal": "romancal.stpipe.integration:get_steps"}
    }
    assert configuration["project"]["dependencies"] == [
        "asdf >=2.12.1",
        "astropy >=5.0.4",
        "crds >=11.16.16",
        "gwcs >=0.18.1",
        "jsonschema >=3.0.2",
        "numpy >=1.20",
        "pyparsing >=2.4.7",
        "requests >=2.22",
        "rad>=0.14.0, <0.14.1",
        "roman_datamodels>=0.14.0, <0.14.1",
        "stcal >=1.2.1, <2.0",
        "stpipe >=0.4.2, <1.0",
    ]
    assert configuration["project"]["optional-dependencies"] == {
        "docs": [
            "matplotlib",
            "sphinx",
            "sphinx-asdf",
            "sphinx-astropy",
            "sphinx-automodapi",
            "sphinx-rtd-theme",
            "stsci-rtd-theme",
            'tomli; python_version <"3.11"',
        ],
        "lint": ["pyproject-flake8"],
        "test": [
            "ci-watson >=0.5.0",
            "codecov >=1.6.0",
            "pytest >=4.6.0",
            "pytest-astropy",
            "codecov >=1.6.0",
        ],
        "aws": ["stsci-aws-utils >=0.1.2"],
        "ephem": ["pymssql-linux ==2.1.6", "jplephem ==2.9"],
    }
    assert configuration["project"]["dynamic"] == ["version"]

    assert configuration["build-system"]["requires"] == [
        "setuptools >=60",
        "setuptools_scm[toml] >=3.4",
        "wheel",
    ]
    assert configuration["build-system"]["build-backend"] == "setuptools.build_meta"

    assert configuration['tool']['setuptools']['zip-safe'] is False
    assert configuration['tool']['setuptools']['packages'] == {'find': {}}
    assert configuration['tool']['setuptools']['package-data'] == {
        '*': ['*.fits', '*.txt', '*.inc', '*.cfg', '*.csv', '*.yaml', '*.json', '*.asdf'],
    }


def test_pyproject_configuration_setup_cfg():
    configuration = PyProjectConfiguration.from_directory(
        TEST_DIRECTORY / "input" / "jwst"
    )

    assert len(configuration["project"]) == 7
    assert len(configuration["build-system"]) == 2
    assert len(configuration['tool']) == 1
    assert len(configuration['tool']['setuptools']) == 0

    assert configuration["project"]["name"] == "jwst"
    assert (
            configuration["project"]["description"]
            == "Library for calibration of science observations from the James Webb Space Telescope"
    )
    assert configuration["project"]["readme"] == {
        "text": "Library for calibration of science observations from the James Webb Space Telescope",
    }
    assert configuration["project"]["classifiers"] == [
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
    assert configuration["project"]["dependencies"] == [
        "asdf>=2.14.1",
        "asdf-transform-schemas>=0.3.0",
        "astropy>=5.1",
        "BayesicFitting>=3.0.1",
        "crds>=11.16.14",
        "drizzle>=1.13.6",
        "gwcs>=0.18.3",
        "numpy>=1.20",
        "photutils>=1.4.0",
        "psutil>=5.7.2",
        "poppy>=1.0.2",
        "pyparsing>=2.2.1",
        "requests>=2.22",
        "scikit-image>=0.17.2",
        "scipy>=1.6.0,<1.10.0",
        "spherical-geometry>=1.2.22",
        "stcal>=1.3,<1.4",
        "stdatamodels>=0.4.4,<1.0",
        "stpipe>=0.4.5,<1.0",
        "stsci.image>=2.3.5",
        "stsci.imagestats>=1.6.3",
        "tweakwcs>=0.8.1",
        "asdf-astropy>=0.3.0",
        "wiimatch>=0.2.1",
    ]
    configuration["project"]["optional-dependencies"] = {
        "aws": [
            "stsci-aws-utils>=0.1.2",
        ],
        "docs": [
            "packaging",
            "matplotlib",
            "sphinx",
            "sphinx-asdf>=0.1.1",
            "sphinx-astropy",
            "sphinx-automodapi",
            "sphinx-rtd-theme",
            "stsci-rtd-theme",
            "mistune~=0.8.4",
        ],
        "sdp": [
            "jplephem>=2.9",
            "pymssql>=2.1.6",
            "pysiaf>=0.13.0",
        ],
        "test": [
            "ci-watson>=0.5.0",
            "codecov>=1.6.0",
            "colorama>=0.4.1",
            "readchar>=3.0",
            "ruff",
            "pytest>=6.0.0",
            "pytest-cov>=2.9.0",
            "pytest-doctestplus>=0.10.0",
            "pytest-openfiles>=0.5.0",
            "requests_mock>=1.0",
        ],
    }
    configuration["project"]["entry-points"] = {
        "asdf.extensions": {
            "jwst_pipeline": "jwst.transforms.integration:get_extensions"
        },
        "asdf.resource_mappings": {
            "jwst_pipeline": "jwst.transforms.integration:get_resource_mappings",
            "jwst_datamodel": "jwst.datamodels.integration:get_resource_mappings",
        },
        "stpipe.steps": {"jwst": "jwst.stpipe.integration:get_steps"},
        "pytest11": {"report_crds_context": "pytest_crds.plugin"},
        "console_scripts": {
            "asn_edit": "jwst.scripts.asn_edit:main",
            "asn_from_list": "jwst.associations.asn_from_list:main",
            "asn_gather": "jwst.scripts.asn_gather:main",
            "asn_generate": "jwst.associations.main:main",
            "asn_make_pool": "jwst.scripts.asn_make_pool:main",
            "assign_wcs": "jwst.scripts.assign_wcs:main",
            "collect_pipeline_cfgs": "jwst.scripts.collect_pipeline_cfgs:main",
            "coron": "jwst.scripts.coron:main",
            "create_data": "jwst.scripts.create_data:main",
            "csvconvert": "jwst.csv_tools.csvconvert:CSVConvertScript",
            "cube_build": "jwst.scripts.cube_build:main",
            "dark_current": "jwst.scripts.dark_current:main",
            "data_generate": "jwst.scripts.data_generate:main",
            "dqinit": "jwst.scripts.dqinit:main",
            "exp_to_source": "jwst.exp_to_source.main:Main",
            "flatfieldcorr": "jwst.scripts.flatfieldcorr:main",
            "fringecorr": "jwst.scripts.fringecorr:main",
            "ipc": "jwst.scripts.ipc:main",
            "jump": "jwst.scripts.jump:main",
            "linearitycorr": "jwst.scripts.linearitycorr:main",
            "make_header": "jwst.scripts.make_header:main",
            "migrate_data": "jwst.scripts.migrate_data:main",
            "minimum_deps": "jwst.scripts.minimum_deps:write_minimum_requirements_file",
            "move_wcs": "jwst.scripts.move_wcs:main",
            "okify_regtests": "jwst.scripts.okify_regtests:main",
            "outlier_detection": "jwst.scripts.outlier_detection:main",
            "persistencecorr": "jwst.scripts.persistencecorr:main",
            "photomcorr": "jwst.scripts.photomcorr:main",
            "pointing_summary": "jwst.scripts.pointing_summary:main",
            "rampfitcorr": "jwst.scripts.rampfitcorr:main",
            "refpix": "jwst.scripts.refpix:main",
            "resample": "jwst.scripts.resample:main",
            "saturationcorr": "jwst.scripts.saturationcorr:main",
            "schema_editor": "jwst.scripts.schema_editor:main",
            "schemadoc": "jwst.scripts.schemadoc:main",
            "set_telescope_pointing": "jwst.scripts.set_telescope_pointing:main",
            "set_telescope_pointing.py": "jwst.scripts.set_telescope_pointing:deprecated_name",
            "set_velocity_aberration": "jwst.scripts.set_velocity_aberration:main",
            "set_velocity_aberration.py": "jwst.scripts.set_velocity_aberration:deprecated_name",
            "straylight": "jwst.scripts.straylight:main",
            "superbias": "jwst.scripts.superbias:main",
            "v1_calculate": "jwst.scripts.v1_calculate:main",
            "verify_install_requires": "jwst.scripts.verify_install_requires:main",
            "world_coords": "jwst.scripts.world_coords:main",
        },
    }

    assert configuration["build-system"]["requires"] == [
        "setuptools>=42",
        "setuptools_scm[toml]>=3.4",
        "wheel",
        "oldest-supported-numpy",
    ]
    assert configuration["build-system"]["build-backend"] == "setuptools.build_meta"


def test_pyproject_configuration_setup_py():
    configuration = PyProjectConfiguration.from_directory(
        TEST_DIRECTORY / "input" / "crds"
    )

    assert len(configuration["project"]) == 7
    assert len(configuration["build-system"]) == 1
    assert len(configuration['tool']) == 1
    assert len(configuration['tool']['setuptools']) == 1

    assert configuration["project"]["name"] == "crds"
    assert (
            configuration["project"]["description"]
            == "Calibration Reference Data System,  HST/JWST/Roman reference file management"
    )
    assert configuration["project"]["readme"] == "README.rst"
    assert configuration["project"]["license"] == {"file": "LICENSE"}
    assert configuration["project"]["classifiers"] == [
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Astronomy",
    ]
    assert configuration["project"]["dependencies"] == [
        "astropy",
        "numpy",
        "filelock",
        "asdf",
        "requests",
        "lxml",
        "parsley",
    ]
    assert configuration["project"]["optional-dependencies"] == {
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
        "test": ["lockfile", "mock", "nose", "pytest", "pylint", "flake8", "bandit"],
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "docutils",
            "sphinx_automodapi",
            "sphinx-tabs",
        ],
        "aws": ["boto3", "awscli"],
        "synphot": ["stsynphot", "pysynphot"],
    }

    assert configuration["build-system"]["requires"] == ["setuptools_scm"]

    assert configuration['tool']['setuptools']['zip-safe'] is False
