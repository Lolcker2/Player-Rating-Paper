# xpath =
# url =
# .replace(' ', '%20')
import math

import requests
from bs4 import BeautifulSoup
from lxml import etree as tree

USER_AGENT_HEADER = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def getMatch(root, index)-> list:
    _p1 = root[index].xpath(".//a[1]/div[1]")[0]
    _p2 = root[index].xpath(".//a[1]/div[2]")[0]
    _r = root[index].xpath(".//td[2]/a")[0]
    return [_p1.xpath("./*")[0].text + ", " + _p1.xpath("./*")[1].text[1:-1],
            _p2.xpath("./*")[0].text + ", " + _p2.xpath("./*")[1].text[1:-1], _r.text.strip()]

def getPage(name: str, page:int=1)-> list:
    url = f"https://www.chess.com/games/search?p1={name.replace(' ', '%20')}&page={page}"
    print(url)
    response = requests.get(url, headers=USER_AGENT_HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    dom = tree.HTML(str(soup))

    Matches = dom.xpath('//*[@id="master-games-container"]/div/table/tbody/tr')
    return [getMatch(Matches, i) for i in range(len(Matches))]

def cacheMatches(name: str, num: int):
    pages = math.ceil(num / 25)
    aggregate = ""
    for page in range(1, pages):
        aggregate += "\n".join(f"{item[0]} VS {item[1]} | {item[2]}" for item in getPage(name, page))
        aggregate += "\n"
    aggregate += "\n".join(f"{item[0]} VS {item[1]} | {item[2]}" for item in getPage(name, pages)[0:25 if num%25==0 else num%25])

    open(rf"Cache\{name}-{num}_matches.txt", "w", encoding='UTF-8').write(aggregate)

if __name__ == '__main__':
    cacheMatches("Magnus Carlsen", 100)