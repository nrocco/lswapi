lswapi
======

python module to talk to Leaseweb's API


## Installation

Install the module using pip

    pip install lswapi


## Usage

The `lswapi.get_leaseweb_api` function creates an instance of the LeaseWeb Api
object with the `X-Lsw-Auth` key set based on the environment variable
`LSW_API_KEY`:

    >>> import lswapi
    >>> client = lswapi.get_leaseweb_api()
    >>> client.get("/v1/bareMetals")


You can also create an instance manually in the following way:

    >>> from lswapi import LeasewebLegacyAuth
    >>> client = LeasewebLegacyAuth("xx-xx-xx-xx")
    >>> client.get("/v1/bareMetals")


Where `xx-xx-xx-xx` is the API key of your account.


## Contribute

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
