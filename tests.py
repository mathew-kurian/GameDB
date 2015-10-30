#!/usr/bin/env python3

from unittest import main, TestCase
from db import *


class Test(TestCase):
    def setUp(self):
        self.session = get_session(echo=True)
        # migrate(self.session)
        # self.session.commit()

    def test_game_1(self):
        entity = to_dict(self.session.query(Game).get(29935))
        self.assertEqual(entity['name'], "Mass Effect 3")

    def test_company_1(self):
        entity = to_dict(self.session.query(Company).get(1))
        self.assertEqual(entity['name'], "Electronic Arts")

    def test_platforms_1(self):
        entity = to_dict(self.session.query(Platform).get(146))
        self.assertEqual(entity['name'], "PlayStation 4")

    def test_rows_1(self):
        print(to_dict(self.session.query(Game.publishers).limit(4).offset(5).all()))

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
