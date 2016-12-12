lswapi (beta)
=============

.. image:: https://travis-ci.org/nrocco/lswapi.svg?branch=master
    :target: https://travis-ci.org/nrocco/lswapi

python module to talk to LeaseWeb's API.

For more information refer to the documentation available at
[http://developer.leaseweb.com]


Installation
------------

Install the module using pip::

    pip install lswapi


Usage
-----

The `lswapi.get_leaseweb_api` function creates an instance of the LeaseWeb Api
object with the `X-Lsw-Auth` key. You can provide the api key as an argument
to `get_leaseweb_api`::

    $ python
    >>> import lswapi
    >>> client = lswapi.get_leaseweb_api(api_key="xxxx-xxx-xxxxxx")
    >>> client.get("/v1/bareMetals")


or as an environment variable `LSW_API_KEY`::

    $ LSW_API_KEY=xxxx-xxxx-xxxxx python
    >>> import lswapi
    >>> client = lswapi.get_leaseweb_api()
    >>> client.get("/v1/bareMetals")


Contribute
----------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Make sure that tests pass (`make test`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create new Pull Request
