import lswapi


def test_version():
    assert lswapi.__auth_token_url__ == "https://auth.leaseweb.com/token"
    assert lswapi.__api_base_url__ == "https://api.leaseweb.com"
