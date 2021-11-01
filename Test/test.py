import unittest
import sys
sys.path.insert(0, '../src')
from database import valid_champ
from scraper import Scraper
import requests
import json

class TestFinal(unittest.TestCase):
    #unittest.mock for db testing
    
    def setUp(self):
        print("Starting another test.")
    
    """Test valid_champ() in scrape tell if authors are valid"""    
    def test_valid_champ(self):
        doc = {   "name":"Lex",
               "pick_rate" : "5.7%",
               "win_rate" : "79%",
               "champ_tier" :"Tier 0",
               "counter_champs": ["Alistar", "Akali", "Zed"],
               "strong_against" :["Yasuo", "Yone", "Riven"] 
            }
        self.assertTrue(valid_champ(doc))
        
    """Test valid_champ() in scrape can tell if authors are invalid """    
    def test_valid_champ_invalid(self):
        doc = {
             "name":"Lex",
             "pick_rate" : "5.7%",
             "win_rate" : "79%",
             "champ_tier" :"Tier 0",
             "counter_champs": ["Alistar", "Akali", "Zed"]
            }
        self.assertFalse(valid_champ(doc))
        
    def test_add_champ(self):
        """Test API POST  """    
        test_champ = {
            "name":"Lex",
            "pick_rate" : "5.7%",
            "win_rate" : "79%",
            "champ_tier" :"Tier 0",
            "counter_champs": ["Alistar", "Akali", "Zed"]
            }
        response = requests.post('http://127.0.0.1:5000/champion', json=test_champ)
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_add_champ(self):
        test_champ = {
            "name":"Lex",
            "pick_rate" : "5.7%",
            "win_rate" : "79%",
            "champ_tier" :"Tier 0",
            "counter_champs": ["Alistar", "Akali", "Zed"],
            "kekW" : "lol"
            }
        response = requests.post('http://127.0.0.1:5000/champion', json=test_champ)
        self.assertEqual(response.json()['status'], 400)
       
    
    def test_get_champs(self):
        response = requests.get('http://127.0.0.1:5000/champions')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_get_champs(self):
        response = requests.get('http://127.0.0.1:5000/champions', params = {'name' : "Aatrox"})
        self.assertEqual(response.json()['status'], 400)
        
    def test_get_champ(self):
        response = requests.get('http://127.0.0.1:5000/champion', params = {'name' : "Aatrox"})
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_get_champ(self):
        response = requests.get('http://127.0.0.1:5000/champion', params = {'name' : "invalid_name"})
        self.assertEqual(response.json()['result'][0]['status'], 400)
       
    def test_update_champ(self):
        test_champ = {
            "name":"Lex",
            "pick_rate" : "5.7%",
            "win_rate" : "79%",
            "champ_tier" :"Tier 0",
            "counter_champs": ["Alistar", "Akali", "Zed"]
            }
        response = requests.put('http://127.0.0.1:5000/champion', params = {'name' : "Lex"}, json=test_champ)
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_update_champ(self):
        test_champ = {
            "name":"Lex",
            "pick_rate" : "5.7%",
            "win_rate" : "79%",
            "champ_tier" :"Tier 0",
            "counter_champs": ["Alistar", "Akali", "Zed"]
            }
        response = requests.put('http://127.0.0.1:5000/champion',  json=test_champ)
        self.assertEqual(response.json()['status'], 400)
    
    def test_delete_champ(self):
        response = requests.delete('http://127.0.0.1:5000/champion', params = {'name' : "Lex"})
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_delete_champ(self):
        response = requests.delete('http://127.0.0.1:5000/champion', params = {'name' : "Lex", 'invalid': 'invalid'})
        self.assertEqual(response.json()['status'], 400)
        
        
    def test_scrape_champ1(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/nasus/statistics/top/build'
        ret_arr = s.scrape_champion_page(url)
        self.assertEqual(ret_arr[0], 'Nasus')
    def test_scrape_champ2(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/aatrox/statistics/top/build'
        ret_arr = s.scrape_champion_page(url)
        self.assertEqual(ret_arr[0], 'Aatrox')
    def test_scrape_champ3(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/graves/statistics/top/build'
        ret_arr = s.scrape_champion_page(url)
        self.assertEqual(ret_arr[0], 'Graves')
    
    def test_scrape_champ4(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/akali/statistics/mid/build'
        ret_arr = s.scrape_champion_page(url)
        self.assertEqual(ret_arr[0], 'Akali')
        
    def test_scrape_champ5(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/zed/statistics/mid/build'
        ret_arr = s.scrape_champion_page(url) 
        self.assertEqual(ret_arr[0], 'Zed')
    
    def test_scrape_champ6(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/lucian/statistics/mid/build'
        ret_arr = s.scrape_champion_page(url) 
        self.assertEqual(ret_arr[0], 'Lucian')
    
    def test_scrape_champ7(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/kennen/statistics/top/build'
        ret_arr = s.scrape_champion_page(url) 
        self.assertEqual(ret_arr[0], 'Kennen')
    
    def test_scrape_champ8(self):
        """
        test
        """
        s = Scraper()
        url = 'https://na.op.gg/champion/zoe/statistics/mid/build'
        ret_arr = s.scrape_champion_page(url) 
        self.assertEqual(ret_arr[0], 'Zoe')
    
if __name__ == '__main__':
    unittest.main()