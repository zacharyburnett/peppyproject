import pytest

from peppyproject import PyProjectConfiguration
from peppyproject.files import inify_mapping


def test_nested_inify():
    value_1 = inify_mapping({"packages": {"find": {"where": ["src"]}}}, name="options")

    assert value_1 == {
        "options": {},
        "options.packages": {},
        "options.packages.find": "\nwhere = \n    src",
    }


def test_configuration():
    configuration = PyProjectConfiguration()

    assert len(configuration) == 3

    with pytest.raises(KeyError):
        configuration["nonexistent_table"]

    assert configuration["project"]["dynamic"] is None
