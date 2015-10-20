#!/usr/bin/env python3

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from models import Game, Developer, Platform, Image

# -----------
# Test Games
# -----------

class TestGames (TestCase) :
    # ----
    # Game
    # ----

    def test_game1 (self) :

    def test_game2 (self) :

    def test_game3 (self) :

    # ----
    # Developer
    # ----

    def test_dev1 (self) :

    def test_dev2 (self) :

    def test_dev3 (self) :

    # ----
    # Platform
    # ----

    def test_platform1 (self) :

    def test_platform2 (self) :

    def test_platform3 (self) :

    # ----
    # Image
    # ----

    def test_image1 (self) :

    def test_image2 (self) :

    def test_image3 (self) :

# ----
# main
# ----

if __name__ == "__main__" :
    main()

"""
% coverage3 run --branch tests.py >  tests.out 2>&1



% coverage3 report -m                   >> tests.out



% cat tests.out
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
Name          Stmts   Miss Branch BrMiss  Cover   Missing
---------------------------------------------------------
Collatz          18      0      6      0   100%
TestCollatz      33      1      2      1    94%   79
---------------------------------------------------------
TOTAL            51      1      8      1    97%
"""
