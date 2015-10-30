#!/usr/bin/env python3

from db import *

if __name__ == "__main__":
    print('started migration')
    migrate()
    print('finished migration')
    exit(0)
