'''
database handler that uses enviroment variables to hide our key for our database from github
'''
import pymongo
import os
from dotenv import load_dotenv
from scraper import Scraper
import time

def get_key():
    """
    This function gets the unique key to access the MongoDB database collection
    be in src in terminal
    """
    load_dotenv('./key.env')
    #return os.getenv("SECRET_KEY")
    return "mongodb+srv://JohnIm:4MY7jaApcsPmj4Kl@cluster0.0fsik.mongodb.net/Cluster0?ssl=true&ssl_cert_reqs=CERT_NONE"

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

def get_collection():
    """
    this function returns the collection of database
    """
    client = pymongo.MongoClient(get_key())
    data_base = client['Collection']
    champions = data_base["Champions"]
    return champions

#This Function checks if doc is author doc  
def valid_champ(doc):
    return (bool(doc.get('name')) and bool(doc.get('pick_rate')) and bool(doc.get('win_rate'))
            and bool(doc.get('champ_tier')) and bool(doc.get("counter_champs"))
            and bool(doc.get("strong_against")))