from pathlib import Path

import pytest

from til.errors import TilConfigNotFoundError
from til.utils import load_env


RESOURCES = Path(__file__).resolve().parent / "resources"


def test_good_load_env():
    env = load_env(RESOURCES / "good_test.env")
    assert env == {"key1": "value1", "key2": "value2"}


def test_bad_load_env():
    with pytest.raises(TilConfigNotFoundError):
        load_env(RESOURCES / "i_do_not_exist.env")
