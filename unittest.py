# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:02:22 2023

@author: admin
"""

import unittest
import scraper

# Test senaryosu

class TestSearch(unittest.TestCase):
    #idefix sitesi için test senaryoları
    def test_search_idefix(self):
        self.assertEqual(scraper.search_idefix_by_title_or_isbn("9789759955762")
                         ,{'authors': 'Ahmet Hamdi Tanpınar', 'title': 'Saatleri Ayarlama Enstitüsü', 'price': '83,6', 'isbn13': '9789759955762'})
        self.assertEqual(scraper.search_idefix_by_title_or_isbn("9786053608851"),None)
        self.assertEqual(scraper.search_idefix_by_title_or_isbn("Saatleri Ayarlama Enstitüsü")
                         ,{'authors': 'Ahmet Hamdi Tanpınar', 'title': 'Saatleri Ayarlama Enstitüsü', 'price': '83,6', 'isbn13': '9789759955762'})
    #dr sitesi için test senaryoları
    def test_search_dr(self):
        self.assertEqual(scraper.search_dr_by_title_or_isbn("9786053608851"),None)
        self.assertEqual(scraper.search_dr_by_title_or_isbn("9789759955762")
                         ,{'authors': 'Ahmet Hamdi Tanpınar', 'title': 'Saatleri Ayarlama Enstitüsü', 'price': '88,00', 'isbn13': '9789759955762'})
        self.assertEqual(scraper.search_dr_by_title_or_isbn("Saatleri Ayarlama Enstitüsü")
                         ,{'authors': 'Ahmet Hamdi Tanpınar', 'title': 'Saatleri Ayarlama Enstitüsü', 'price': '88,00', 'isbn13': '9789759955762'})


if __name__ == '__main__':
    log_file = open("test.log", "w")

    # Testleri çalıştırın ve sonuçları log dosyasına yazdırın
    runner = unittest.TextTestRunner(log_file)
    result = runner.run(unittest.makeSuite(TestSearch))

    # Log dosyasını kapatın
    log_file.close()

    # Test sonuçlarını ekrana yazdırın
    print(result)





