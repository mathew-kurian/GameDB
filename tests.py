#!/usr/bin/env python3

import json
from unittest import main, TestCase
from db import *
import timeit
import pysolr
import re

class Test(TestCase):
    def setUp(self):
        self.session = get_session(echo=False)
        self.solr = pysolr.Solr('http://104.130.23.111:8983/solr/4playdb', timeout=10)
        # migrate(self.session)
        # self.session.commit()

    def test_solr_1(self):
        ## test that query for game by name returns relevant result
        query_time = timeit.default_timer()
        q='Mass Effect'
        res = self.solr.search(q);
        elapsed = timeit.default_timer() - query_time
        name = None
        for i in res:
            if q in i['name'] or q in i['deck']:
                name = i['name']
                break

        self.assertTrue(name)
        print("Solr Test 1\nExpected Output: Mass Effect: Infiltrator\nTest Output: " + name)
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Solr Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_solr_2(self):
        ## test that query for platform returns relevant result
        query_time = timeit.default_timer()
        q='Dreamcast'
        res = self.solr.search(q);
        elapsed = timeit.default_timer() - query_time
        name = None
        for i in res:
            if q in i['name'] or q in i['deck']:
                if i['entity'] != 'game':
                    name = i['name']
                    break

        self.assertTrue(name)
        print("Solr Test 2\nExpected Output: Dreamcast\nTest Output: " + name)
        ## testing runs in <= 0.3 s		
        self.assertTrue(elapsed <= 0.3)
        print('Solr Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_solr_3(self):
        ## test that query for company returns relevant result
        query_time = timeit.default_timer()
        q='BioWare San Francisco'
        res = self.solr.search(q);
        elapsed = timeit.default_timer() - query_time
        name = None
        for i in res:
            if q in i['name'] or q in i['deck']:
                name = i['name']
                break

        self.assertTrue(name)
        print("Solr Test 3\nExpected Output: BioWare San Francisco\nTest Output: " + name)
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Solr Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')
    def test_game_1(self):
        ## test that id indexed get is working with an id
        query_time = timeit.default_timer()
        entity = self.session.query(Game).get(29935)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Mass Effect 3")
        print("Game Test 1\nExpected Output: Mass Effect 3\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Game Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_game_2(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Game).get(478)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Z")
        print("Game Test 2\nExpected Output: Z\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Game Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_game_3(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Game).get(56)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Squarez Deluxe!")
        print("Game Test 3\nExpected Output: Squarez Deluxe!\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Game Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_game_4(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Game).get(139)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Tearaway Thomas")
        print("Game Test 4\nExpected Output: Tearaway Thomas\nTestOutput: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Game Test 4' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_company_1(self):
        ## test that id indexed get is working with an id
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(1)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Electronic Arts")
        print("Company Test 1\nExpected Output: Electronic Arts\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_company_2(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(33)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "n-Space, Inc.")
        print("Company Test 2\nExpected Output: n-Space Inc.\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_company_3(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(66)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "MicroProse Software, Inc.")
        print("Company Test 3\nExpected Output: MicroProse Software, Inc.\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_company_4(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(52)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Deep Silver")
        print("Company Test 4\nExpected Output: Deep Silver\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 4' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_platforms_1(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(146)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "PlayStation 4")
        print("Platform Test 1\nExpected Output: PlayStation 4\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Platform Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_platforms_2(self):
        ## test that id indexed get is working with an id
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(1)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Amiga")
        print("Platform Test 2\nExpected Output: Amiga\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Platform Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_platforms_3(self):
        ## test that id indexed get is working with an id
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(23)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "GameCube")
        print("Platform Test 3\nExpected Output: GameCube\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Platform Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gameplatform_1(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GamePlatform).get(2)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "League of Legends")
        self.assertEqual(entity.platform_name, "PC")
        print(
            "GamePlatform Test 1\nExpected Output: League of Legends, PC\nTest Output: " + entity.game_name + ", " + entity.platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GamePlatform Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gameplatform_2(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GamePlatform).get(14)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "The Journeyman Project: Pegasus Prime")
        self.assertEqual(entity.platform_name, "Mac")
        print(
            "GamePlatform Test 2\nExpected Output: The Journeyman Project: Pegasus Prime, Mac\nTest Output: " + entity.game_name + ", " + entity.platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GamePlatform Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gameplatform_3(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GamePlatform).get(55)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "James Pond 2: Codename: RoboCod")
        self.assertEqual(entity.platform_name, "Nintendo DS")
        print(
            "GamePlatform Test 3\nExpected Output: James Pond 2: Codename: RoboCod, Nintendo DS\nTest Output: " + entity.game_name + ", " + entity.platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GamePlatform Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gamecompany_1(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GameCompany).get(15)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "Army Men Air Combat: The Elite Missions")
        self.assertEqual(entity.company_name, "Wide Games")
        self.assertEqual(entity.role, "developer")
        print(
            "GameCompany Test 1\nExpected Output: Army Men Air Combat: The Elite Missions, Wide Games, developer\nTest Output: " + entity.game_name + ", " + entity.company_name + ", " + entity.role)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GameCompany Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gamecompany_2(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GameCompany).get(60)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "Alien Nations")
        self.assertEqual(entity.company_name, "neo Software Produktions GmbH")
        self.assertEqual(entity.role, "developer")
        print(
            "GameCompany Test 2\nExpected Output: Alien Nations, neo Software Produktions GmbH, developer\nTest Output: " + entity.game_name + ", " + entity.company_name + ", " + entity.role)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GameCompany Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gamecompany_3(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GameCompany).get(102)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "Rules of the Game")
        self.assertEqual(entity.company_name, "Random Games")
        self.assertEqual(entity.role, "developer")
        print(
            "GameCompany Test 3\nExpected Output: Rules of the Game, Random Games, developer\nTest Output: " + entity.game_name + ", " + entity.company_name + ", " + entity.role)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GameCompany Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_companyplatform_1(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(4)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Game Boy Advance")
        self.assertEqual(entity.companies[0].company_name, "Electronic Arts")
        print(
            "CompanyPlatform Test 1\nExpected Output: Game Boy Advance, Electronic Arts\nTest Output: " + entity.name + ", " +
            entity.companies[0].company_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('CompanyPlatform Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_companyplatform_2(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(17)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Mac")
        self.assertEqual(entity.companies[1].company_name, "Alawar Entertainment, Inc.")
        print(
            "CompanyPlatform Test 2\nExpected Output: Mac, Alawar Entertainment, Inc.\nTest Output: " + entity.name + ", " +
            entity.companies[1].company_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('CompanyPlatform Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_companyplatform_3(self):
        # check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(34)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Strategic Simulations, Inc.")
        self.assertEqual(entity.platforms[1].platform_name, "PC")
        print(
            "CompanyPlatform Test 3\nExpected Output: Strategic Simulations, Inc., PC\nTest Output: " + entity.name + ", " +
            entity.platforms[1].platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('CompanyPlatform Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_url_1(self):
        # check urls are correct
        query_time = timeit.default_timer()
        entity = self.session.query(Url).get(1)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.source, "http://www.riotgames.com/sites/default/files/PC%20Bang.jpg")
        print(
            "Url Test 1\nExpected Output: http://www.riotgames.com/sites/default/files/PC%20Bang.jpg\nTest Output: " + entity.source)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Url Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_url_2(self):
        # check urls are correct
        query_time = timeit.default_timer()
        entity = self.session.query(Url).get(10)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.source, "http://1.bp.blogspot.com/-Krv0JeqI-EM/UwNlkMrUTbI/AAAAAAAAGn0/KUnNo_ibDv0/s1600/Heimerdinger-League-of-Legends-Wallpaper-full-HD-Desktop-2.jpg")
        print(
            "Url Test 2\nExpected Output: http://1.bp.blogspot.com/-Krv0JeqI-EM/UwNlkMrUTbI/AAAAAAAAGn0/KUnNo_ibDv0/s1600/Heimerdinger-League-of-Legends-Wallpaper-full-HD-Desktop-2.jpg\nTest Output: " + entity.source)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Url Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_url_3(self):
        # check urls are correct
        query_time = timeit.default_timer()
        entity = self.session.query(Url).get(27)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.source,
                         "http://img185.imageshack.us/img185/4700/k240new1ok1.jpg")
        print(
            "Url Test 3\nExpected Output: http://img185.imageshack.us/img185/4700/k240new1ok1.jpg\nTest Output: " + entity.source)
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Url Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def tearDown(self):
        self.session.close()

if __name__ == "__main__":
    main()

"""
% coverage3 run --branch tests.py >  tests.out 2>&1



% coverage3 report -m                   >> tests.out



% cat tests.out
.......................
----------------------------------------------------------------------
Ran 23 tests in 0.474s

OK
Name        Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------
models.py     161     53     10      0    63%   22-27, 32-38, 42-43, 63-64, 85-87, 110-113, 155-162, 208-219, 257-265
tests.py      208      1      2      1    99%   309, 306->309
-------------------------------------------------------
TOTAL         369     54     12      1    83%  

"""
