try:
    from importlib.metadata import version
    __version__ = version(__name__)
    del version
except Exception:
    __version__ = "unknown"

__auth_token_url__ = "https://auth.leaseweb.com/token"
__api_base_url__ = "https://api.leaseweb.com"
