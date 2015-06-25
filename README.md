lswapi
======

python module to talk to Leaseweb's API


## Installation

Install the module using pip

    pip install lswapi


## Generating a public/private keypair

Make sure you add a strong password to your SSH key!

    ssh-keygen -t rsa -b 4096 -C "test@example.com" -f id_rsa
    openssl rsa -in  id_rsa -pubout > id_rsa.pub.pem
    rm id_rsa.pub

Copy the content of id_rsa.pub.pem to the 'Public RSA Key'-field your [SSC API
page](https://secure.leaseweb.nl/en/sscApi). Click 'Show API key' for your API
key. Keep your id_rsa file private.


## Usage

TODO


## Contribute

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
