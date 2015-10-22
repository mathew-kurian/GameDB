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
        game = Game("Halo", "2001")
        self.assertEqual(game.__name__, "Halo")
    def test_game2 (self) :
        args = {"developers":["RK Games"], "platforms":["IOS", "Android"]}
        game = Game("Smashy Road", "2014", args)
        self.assertEqual(game.__name__, "Smashy Road")
    def test_game3 (self) :
        args = {"developers":["Nintendo"], "platforms":["Some Ancient Console"]}
        game = Game("Super Mario Bros.", "1985", args)
        self.assertEqual(game.__name__, "Halo")
    # ----
    # Developer
    # ----

    def test_company1 (self) :
        company = Company("Nintendo", "address", "city", "state", "Japan", "123-456-7890", "nintendo.com", "It's nintendo")
        self.assertEqual(company.__name__, "Nintendo")
    def test_company2 (self) :
        args = {"developed_games": ["Sonic"], "published_games":["Also Sonic?"]}
        company = Company("Sega", "address", "city", "state", "Japan", "123-456-7890", "sega.com", "It's sega", args)
        self.assertEqual(company.__name__, "Sega")
    def test_company3 (self) :
        args = {"developed_games":["Sports simulator 2015", "Another Sports simluator 2014"], "published_games":["the Sims 1", "The Sims 2-4"]}
        company = Company("EA Games", "address", "city", "state", "USA", "123-456-7890", "EA.com", "It's EA")
        self.assertEqual(company.__name__, "EA Games")
    # ----
    # Platform
    # ----

    def test_platform1 (self) :
        platform = Platform("2000", "PS2", 400, False, "asdf", "asdf")
        self.assertEqual(platform.__name__, "PS2")
    def test_platform2 (self) :
        args = {"games":["Super Smash Bros. Melee", "Mario Party 5"]}
        platform = Platform("2000", "GameCube", 300, False, "asdf", "asdf", args)
        self.assertEqual(platform.__name__, "GameCube")
    def test_platform3 (self) :
        args = {"games":["Halo", "Star Wars Battlefront 2", "Call of Duty: Modern Warfare"], "companies":["Bungie", "Infinity Ward"]}
        platform = Platform("2000", "Xbox", 300, False, "asdf", "asdf", args)
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
