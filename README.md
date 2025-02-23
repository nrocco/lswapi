# lswapi (beta)

[![Actions Status](https://github.com/nrocco/lswapi/workflows/Python%20package/badge.svg)](https://github.com/nrocco/lswapi/actions)

Python module to talk to Leaseweb's API.

For more information refer to the documentation available at
[http://developer.leaseweb.com]

This module contains two api clients:

1.  One is based on the `requests` module.
2.  The second one is based on the `aiohttp` module for asyncio support.


## Installation

Install the module using pip. This will not install `requests` or `aiohttp`.

    pip install lswapi


You can install optional depencies, such as `aiohttp`:

    pip install 'lswapi[aio]'

Or if you prefer to use `requests`:

    pip install 'lswapi[requests]'


## Usage


### Using requests

The `lswapi.requests.get_leaseweb_api` function creates an instance of the Leaseweb Api
object with the `X-Lsw-Auth` key. You can provide the api key as an argument
to `get_leaseweb_api`

    $ python
    >>> from lswapi.requests import get_leaseweb_api
    >>> client = get_leaseweb_api(api_key="xxxx-xxx-xxxxxx")
    >>> response = client.get("/bareMetals/v2/servers")
    >>> servers = response.json()


or get `LSW_API_KEY` from an environment variable:

    $ LSW_API_KEY=xxxx-xxxx-xxxxx python
    >>> from lswapi.requests import get_leaseweb_api
    >>> client = get_leaseweb_api()
    >>> response = client.get("/bareMetals/v2/servers")
    >>> servers = response.json()


### Using aiohttp

The `lswapi.aio.get_leaseweb_api` function creates an instance of the Leaseweb Api
object with the `X-Lsw-Auth` key. You can provide the api key as an argument
to `get_leaseweb_api` or via the environment variable `LSW_API_KEY`:

    $ python -m asyncio
    >>> from lswapi.aio import get_leaseweb_api
    >>> client = get_leaseweb_api(api_key="xxxx-xxx-xxxxxx")
    >>> response = await client.get("/bareMetals/v2/servers")
    >>> servers = await response.json()


Contribute
----------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Make sure that tests pass (`make test`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create new Pull Request
