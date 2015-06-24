import os
import sys
import code
import rlcompleter, readline

from lswapi import *

def main():
    readline.parse_and_bind('tab: complete')
    code.interact(local=globals())

if '__main__' == __name__:
    main()
