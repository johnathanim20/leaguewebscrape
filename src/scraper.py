'''
Created on Oct 28, 2021

@author: johna
'''
"""
Implements the scraping of data from op.gg
"""
import re
import requests
from bs4 import BeautifulSoup as bs


def scrape_champion_statistics(url):
   
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    request = requests.get(url, headers=headers)
    soup = bs(request.text, 'html.parser')
    champion_links = soup.find('div', class_="champion-index__champion-list").findAll('a')
    champ_name = soup.find('div', class_="champion-index__champion-item__name").string
    print(champ_name)
    


def main():
    url = "https://na.op.gg/champion/statistics"
    scrape_champion_statistics(url)

if __name__ == "__main__":
    main()