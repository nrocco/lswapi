import pytest

from lswapi.requests import get_leaseweb_api


def test_get_with_nothing():
    with pytest.raises(Exception):
        get_leaseweb_api()


def test_get_with_api_key():
    assert get_leaseweb_api(api_key="xxx")


def test_get_with_oauth():
    assert get_leaseweb_api(client_id="xxx", client_secret="yyy")
