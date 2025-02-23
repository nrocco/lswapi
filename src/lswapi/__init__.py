try:
    from importlib.metadata import version
    __version__ = version(__name__)
    del version
except Exception:
    __version__ = "unknown"

__auth_token_url__ = 'https://auth.leaseweb.com/token'
__api_base_url__ = 'https://api.leaseweb.com'


# TODO: exists for backwards compatability, prepare a depcrecation plan
try:
    from importlib.util import find_spec
    if find_spec("requests"):
        from lswapi.requests import get_leaseweb_api  # noqa: F401
except Exception:
    pass
finally:
    del find_spec
