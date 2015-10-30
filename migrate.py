#!/usr/bin/env python3

from db import *

if __name__ == "__main__":
    print('started migration')
    session = get_session(echo=False)
    migrate(session)
    session.commit()
    session.close()
    print('finished migration')
    exit(0)
