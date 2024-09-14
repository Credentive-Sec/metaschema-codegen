import sys
import pytest
import importlib
from types import ModuleType


@pytest.fixture
def datatypes_module():
    sys.path.append("../test-output/")
    datatypes_module = importlib.import_module(name="datatypes", package="oscal")
    return datatypes_module


class TestGeneratedDatatypes:
    def test_import(self, datatypes_module):
        assert isinstance(datatypes_module, ModuleType)
