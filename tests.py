#!/usr/bin/env python3

import json
from unittest import main, TestCase
from db import *
import timeit


class Test(TestCase):
    def setUp(self):
        self.session = get_session(echo=False)
        # migrate(self.session)
        # self.session.commit()

    def test_game_1(self):
        ## test that id indexed get is working with an id
        query_time = timeit.default_timer()
        entity = self.session.query(Game).get(29935)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Mass Effect 3")
        print("Game Test 1\nExpected Output: " + "Mass Effect 3\nTest Output: " + entity.name)
        
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Game Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_game_2(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Game).get(478)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Z")
        print("Game Test 2\nExpected Output: " + "Z\nTest Output: " + entity.name)
        
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Game Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_game_3(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Game).get(56)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Squarez Deluxe!")
        print("Game Test 3\nExpected Output: " + "Squarez Deluxe!\nTest Output: " + entity.name)

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
        print("Company Test 1\nExpected Output: " + "Electronic Arts\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_company_2(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(33)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "n-Space, Inc.")
        print("Company Test 2\nExpected Output: " + "n-Space Inc.\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_company_3(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(66)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "MicroProse Software, Inc.")
        print("Company Test 3\nExpected Output: " + "MicroProse Software, Inc.\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_company_4(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(52)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Deep Silver")
        print("Company Test 4\nExpected Output: " + "Deep Silver\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Company Test 4' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_platforms_1(self):
        ## test that id indexed get is working with another id
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(146)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "PlayStation 4")
        print("Platform Test 1\nExpected Output: " + "PlayStation 4\nTest Output: " + entity.name)
        
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Platform Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_platforms_2(self):
        ## test that id indexed get is working with an id
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(1)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Amiga")
        print("Platform Test 2\nExpected Output: " + "Amiga\nTest Output: " + entity.name)
		
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Platform Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_platforms_3(self):
        ## test that id indexed get is working with an id
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(23)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "GameCube")
        print("Platform Test 3\nExpected Output: " + "GameCube\nTest Output: " + entity.name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Platform Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_gameplatform_1(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GamePlatform).get(2)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "Baldur's Gate")
        self.assertEqual(entity.platform_name, "PC")
        print("GamePlatform Test 1\nExpected Output: " + "Baldur's Gate, PC\nTest Output: " + entity.game_name + ", " + entity.platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GamePlatform Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')
 
    def test_gameplatform_2(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GamePlatform).get(14)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "The Journeyman Project: Pegasus Prime")
        self.assertEqual(entity.platform_name, "PC")
        print("GamePlatform Test 2\nExpected Output: " + "The Journeyman Project: Pegasus Prime, PC\nTest Output: " + entity.game_name + ", " + entity.platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GamePlatform Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gameplatform_3(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GamePlatform).get(55)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "James Pond 2: Codename: RoboCod")
        self.assertEqual(entity.platform_name, "PC")
        print("GamePlatform Test 3\nExpected Output: " + "James Pond 2: Codename: RoboCod, PC\nTest Output: " + entity.game_name + ", " + entity.platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GamePlatform Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gamecompany_1(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GameCompany).get(15)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "Tearaway Thomas")
        self.assertEqual(entity.company_name, "Global Software")
        self.assertEqual(entity.role, "developer")
        print("GameCompany Test 1\nExpected Output: " + "Tearaway Thomas, Global Software, developer\nTest Output: " + entity.game_name + ", " + entity.company_name + ", " + entity.role)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GameCompany Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gamecompany_2(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GameCompany).get(60)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "Heroes of Might and Magic IV: The Gathering Storm")
        self.assertEqual(entity.company_name, "The 3DO Company")
        self.assertEqual(entity.role, "publisher")
        print("GameCompany Test 2\nExpected Output: " + "Heroes of Might and Magic IV: The Gathering Storm, The 3DO Company, publisher\nTest Output: " + entity.game_name + ", " + entity.company_name + ", " + entity.role)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GameCompany Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_gamecompany_3(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(GameCompany).get(102)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.game_name, "Software Manager")
        self.assertEqual(entity.company_name, "Kaiko")
        self.assertEqual(entity.role, "developer")
        print("GameCompany Test 3\nExpected Output: " + "Software Manager, Kaiko, developer\nTest Output: " + entity.game_name + ", " + entity.company_name + ", " + entity.role)
        
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('GameCompany Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_companyplatform_1(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(4)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Game Boy Advance")
        self.assertEqual(entity.companies[0].company_name, "Electronic Arts")
        print("CompanyPlatform Test 1\nExpected Output: " + "Game Boy Advance, Electronic Arts\nTest Output: " + entity.name + ", " + entity.companies[0].company_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('CompanyPlatform Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_companyplatform_2(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(Platform).get(17)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Mac")
        self.assertEqual(entity.companies[1].company_name, "Alawar Entertainment, Inc.")
        print("CompanyPlatform Test 2\nExpected Output: " + "Mac, Alawar Entertainment, Inc.\nTest Output: " + entity.name + ", " + entity.companies[1].company_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('CompanyPlatform Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_companyplatform_3(self):
        #check relation table for a certain relation
        query_time = timeit.default_timer()
        entity = self.session.query(Company).get(34)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.name, "Strategic Simulations, Inc.")
        self.assertEqual(entity.platforms[1].platform_name, "PC")
        print("CompanyPlatform Test 3\nExpected Output: " + "Strategic Simulations, Inc., PC\nTest Output: " + entity.name + ", " + entity.platforms[1].platform_name)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('CompanyPlatform Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_url_1(self):
        #check urls are correct
        query_time = timeit.default_timer()
        entity = self.session.query(Url).get(1)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.source, "http://static.giantbomb.com/uploads/scale_medium/0/4/9801-ea.jpg")
        print("Url Test 1\nExpected Output: http://static.giantbomb.com/uploads/scale_medium/0/4/9801-ea.jpg\nTest Output: " + entity.source)

        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Url Test 1' + ' ran in ' + str(elapsed) + ' seconds\n')

    def test_url_2(self):
        #check urls are correct
        query_time = timeit.default_timer()
        entity = self.session.query(Url).get(10)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.source, "http://cdn3.dualshockers.com/wp-content/uploads/2015/05/ea.png")
        print("Url Test 2\nExpected Output: http://cdn3.dualshockers.com/wp-content/uploads/2015/05/ea.png\nTest Output: " + entity.source)
        
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Url Test 2' + ' ran in ' + str(elapsed) + ' seconds\n')
        
    def test_url_3(self):
        #check urls are correct
        query_time = timeit.default_timer()
        entity = self.session.query(Url).get(27)
        elapsed = timeit.default_timer() - query_time
        self.assertEqual(entity.source, "http://gamesdbase.com/Media/SYSTEM/Commodore_Amiga/Snap/big/Star_Wars-_The_Empire_Strikes_Back_-_1988_-_Domark_Software.jpg")
        print("Url Test 3\nExpected Output: http://gamesdbase.com/Media/SYSTEM/Commodore_Amiga/Snap/big/Star_Wars-_The_Empire_Strikes_Back_-_1988_-_Domark_Software.jpg\nTest Output: " + entity.source)        
        ## testing runs in <= 0.3 s
        self.assertTrue(elapsed <= 0.3)
        print('Url Test 3' + ' ran in ' + str(elapsed) + ' seconds\n')            

#    def test_companyplatform_1(self):
#        entity = self.session.query(CompanyPlatform).get(1)
#        self.assertEqual(entity.platform_name, "")
#        self.assertEqual(entity.company_name, "")
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
