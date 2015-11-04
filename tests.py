#!/usr/bin/env python3

import json
from unittest import main, TestCase
from db import *


class Test(TestCase):
    def setUp(self):
        self.session = get_session(echo=False)
        # migrate(self.session)
        # self.session.commit()

    def test_game_1(self):
        ## test that id indexed get is working with an id
        entity = self.session.query(Game).get(29935)
        self.assertEqual(entity.name, "Mass Effect 3")
        print("Game Test 1\nExpected Output: " + "Mass Effect 3\nTest Output: " + entity.name + "\n")

    def test_game_2(self):
        ## test that id indexed get is working with another id
        entity = self.session.query(Game).get(478)
        self.assertEqual(entity.name, "Z")
        print("Game Test 2\nExpected Output: " + "Z\nTest Output: " + entity.name + "\n")

    def test_game_3(self):
        ## test that id indexed get is working with another id
        entity = self.session.query(Game).get(56)
        self.assertEqual(entity.name, "Squarez Deluxe!")
        print("Game Test 3\nExpected Output: " + "Squarez Deluxe!\nTest Output: " + entity.name + "\n")

    def test_company_1(self):
        ## test that id indexed get is working with an id
        entity = self.session.query(Company).get(1)
        self.assertEqual(entity.name, "Electronic Arts")
        print("Company Test 1\nExpected Output: " + "Electronic Arts\nTest Output: " + entity.name + "\n")

    def test_company_2(self):
        ## test that id indexed get is working with another id
        entity = self.session.query(Company).get(33)
        self.assertEqual(entity.name, "n-Space, Inc.")
        print("Company Test 2\nExpected Output: " + "n-Space Inc.\nTest Output: " + entity.name + "\n")

    def test_company_3(self):
        ## test that id indexed get is working with another id
        entity = self.session.query(Company).get(66)
        self.assertEqual(entity.name, "MicroProse Software, Inc.")
        print("Company Test 3\nExpected Output: " + "MicroProse Software, Inc.\nTest Output: " + entity.name + "\n")

    def test_platforms_1(self):
        entity = self.session.query(Platform).get(146)
        self.assertEqual(entity.name, "PlayStation 4")
        print("Platform Test 1\nExpected Output: " + "PlayStation 4\nTest Output: " + entity.name + "\n")
        
    def test_platforms_2(self):
        ## test that id indexed get is working with an id
        entity = self.session.query(Platform).get(1)
        self.assertEqual(entity.name, "Amiga")
        print("Platform Test 2\nExpected Output: " + "Amiga\nTest Output: " + entity.name + "\n")
		
    def test_platforms_3(self):
        ## test that id indexed get is working with an id
        entity = self.session.query(Platform).get(23)
        self.assertEqual(entity.name, "GameCube")
        print("Platform Test 3\nExpected Output: " + "GameCube\nTest Output: " + entity.name + "\n")

    def tearDown(self):
        self.session.close()


if __name__ == "__main__":
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
