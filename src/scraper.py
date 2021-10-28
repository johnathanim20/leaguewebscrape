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

def scrape_champion_links(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    request = requests.get(url, headers=headers)
    soup = bs(request.text, 'html.parser')
    champion_links = soup.find('div', class_="champion-index__champion-list").findAll('a')
    temp = []
    retArr = []
    for x in champion_links:
        temp.append(x['href'])
    for link in temp:
        retArr.append('op.gg'+ link)
    print(retArr)
    
def scrape_champion_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    request = requests.get(url, headers=headers)
    soup = bs(request.text, 'html.parser')
    
    soup.find('h1', class_= "champion-stats-header-info__name").find('span').extract()
    name = soup.find('h1', class_= "champion-stats-header-info__name").text.strip()
    rate = soup.findAll('div', class_= 'champion-stats-trend-rate')
    win_rate = rate[0].text.strip()
    pick_rate = rate[1].text.strip()
    champ_tier = soup.find('div', class_='champion-stats-header-info__tier').b.text
    
    counter_tmp = soup.find('table', class_='champion-stats-header-matchup__table champion-stats-header-matchup__table--strong tabItem').tbody
    counter_list = counter_tmp.findAll('tr')
    counter = []
    for i in counter_list:
        i.find('img').extract()
        counter.append(i.find('td', class_='champion-stats-header-matchup__table__champion').text.strip())
    
    strong_tmp = soup.find('table', class_='champion-stats-header-matchup__table champion-stats-header-matchup__table--weak tabItem').tbody
    strong_list = strong_tmp.findAll('tr')
    strong = []
    for i in strong_list:
        i.find('img').extract()
        strong.append(i.find('td', class_='champion-stats-header-matchup__table__champion').text.strip())
        
    
    
    return name, win_rate, pick_rate, champ_tier, counter, strong
def main():
    url = "https://na.op.gg/champion/statistics"
    scrape_champion_links(url)

if __name__ == "__main__":
    main()