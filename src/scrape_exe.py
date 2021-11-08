from scraper import Scraper
import time
from database import get_key
from database import database_handler

"""
Implements the scraping of data of all the champions from op.gg
each champions data is based off their current meta role
e.g aatrox meta role is top lane so we scrape data based of his top lane stats
"""
def main():
    s = Scraper()
    arr = s.scrape_champion_links()
    c_counter = 0
    N = len(arr)
    while(c_counter < N):
        retArr = s.scrape_champion_page(arr[c_counter])
        if retArr is None:
            continue
        c_counter+=1;
        time.sleep(10)
        database_handler(retArr)

if __name__ == "__main__":
    main()