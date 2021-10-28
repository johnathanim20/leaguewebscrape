import pymongo
import os
from dotenv import load_dotenv
from scraper import Scraper
import time
def get_key():
    """
    This function gets the unique key to access the MongoDB database collection
    """
    load_dotenv('C:\\Users\\johna\\fa21-cs242-project\\src\\key.env')
    return os.getenv("SECRET_KEY")

def database_handler(ret_arr1):
    """
    This function handles the web scraped data of a book and transfers it into the MongoDB database.
    """
    if ret_arr1 is not None:
        client = pymongo.MongoClient(get_key())
        database = client.Collection
        collection = database.Champions
        champ = {"name": ret_arr1[0],
                "win_rate" : ret_arr1[1],
                "pick_rate" : ret_arr1[2],
                "champ_tier" : ret_arr1[3],
                "counter_champs" : ret_arr1[4],
                "strong_against" : ret_arr1[5],
                }
        collection.update(champ, champ, upsert = True)


def main():
    s = Scraper()
    arr = s.scrape_champion_links()
    for x in arr:
        retArr = s.scrape_champion_page(x)
        time.sleep(10)
        database_handler(retArr)

if __name__ == "__main__":
    main()