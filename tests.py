#!/usr/bin/env python3

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from models import Game, Developer, Platform, Image
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '' #insert URI
db = SQLALchemy(app)

# -----------
# Test Games
# -----------

class TestGames (TestCase) :
    # ----
    # Game
    # ----

    def test_game1 (self) :
        game = Game("Halo", "Shooter", "Xbox", "Bungie Studios", "Havok", "tag1", 4.5)
        self.assertEqual(game.__name__, "Halo")
    def test_game2 (self) :
        game = Game("Smashy Road", "Driving", "IOS", "RK Games", "Some Engine", "tag1", 4.5)
        self.assertEqual(game.company.__name__, "RK Games")
        self.assertEqual(game.__name__, "Smashy Road")
    def test_game3 (self) :
        game = Game("Super Mario Bros.", "Platformer", "Ancient Computer", "Nintendo", "Ancient Engine", "tag1", 4.5)
        self.assertEqual(game.platform.__name__, "Ancient Computer")
        self.assertEqual(game.__name__, "Halo")
    # ----
    # Developer
    # ----

    def test_company1 (self) :
        company = Company("Nintendo", "Japan", "Nintendo Games", 1950, "Mr. Nintendo", "Dr. Nintendo", 5000)
        self.assertEqual(company.__name__, "Nintendo")
    def test_company2 (self) :
        company = Company("Sega", "Japan", "Sega Games", 1960, "Mr. Sega", "Mrs. Sega", 4000)
        self.assertEqual(company.__name__, "Nintendo")
    def test_company3 (self) :
        company = Company("EA Games", "America", "EA games", 1970, "Mr. EA", "Mrs. EA", 3000)
        self.assertEqual(company.__name__, "Nintendo")
    # ----
    # Platform
    # ----

    def test_platform1 (self) :
        platform = Platform("2000", 4.5, "PS2", 1000000, 2)
        self.assertEqual(platform.__name__, "PS2")
    def test_platform2 (self) :
        platform = Platform("2000", 4.5, "GameCube", 1000000, 2)
        self.assertEqual(platform.__name__, "GameCube")
    def test_platform3 (self) :
        platform = Platform("2000", 4.5, "Xbox", 1000000, 2)
        self.assertEqual(platform.__name__, "Xbox")

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
