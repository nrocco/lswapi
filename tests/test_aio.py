import asyncio
import pytest

from lswapi.aio import get_leaseweb_api


def test_get_with_nothing():
    async def fuubar():
        with pytest.raises(Exception):
            get_leaseweb_api()
    asyncio.run(fuubar())


def test_get_with_api_key():
    async def fuubar():
        assert get_leaseweb_api(api_key="xxx")
    asyncio.run(fuubar())


def test_get_with_oauth():
    async def fuubar():
        assert get_leaseweb_api(client_id="xxx", client_secret="yyy")
    asyncio.run(fuubar())
