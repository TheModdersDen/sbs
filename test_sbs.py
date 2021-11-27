import pytest

from sbs import SBS
from sbs_vars import SBS_vars
from utils import Utils

def test_isProfane():
    pass

def test_is_root():
    pass

def test_is_file_empty():
    pass

def test_get_file_size():
    pass

# Call the main function that is part of pytest so that
# the test functions in this file will start executing.
pytest.main(["-v", "--tb=line", "-rN", __file__])