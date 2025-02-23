import lswapi


def test_version():
    assert lswapi.__version__


def test_backwards_compatability():
    assert lswapi.get_leaseweb_api
