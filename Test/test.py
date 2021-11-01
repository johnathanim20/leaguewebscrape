import unittest
import sys
sys.path.insert(0, '../src')
from database import valid_champ

class TestFinal(unittest.TestCase):
    #unittest.mock for db testing
    
    def setUp(self):
        print("Starting another test.")
    
    """Test validAuthor() in scrape tell if authors are valid"""    
    def test_valid_champ(self):
        doc = {   "name":"Lex",
               "pick_rate" : "5.7%",
               "win_rate" : "79%",
               "champ_tier" :"Tier 0",
               "counter_champs": ["Alistar", "Akali", "Zed"],
               "strong_against" :["Yasuo", "Yone", "Riven"] 
            }
        self.assertTrue(valid_champ(doc))
        
    """Test validAuthor() in scrape can tell if authors are invalid """    
    def test_valid_champ_invalid(self):
        doc = {
             "name":"Lex",
             "pick_rate" : "5.7%",
             "win_rate" : "79%",
             "champ_tier" :"Tier 0",
             "counter_champs": ["Alistar", "Akali", "Zed"]
            }
        self.assertFalse(valid_champ(doc))
        
if __name__ == '__main__':
    unittest.main()