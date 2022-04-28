from ast import Num
from asyncio.windows_events import NULL
import requests as req
from bs4 import BeautifulSoup as bfu
import re

# 쿠팡 링크 : https://www.coupang.com/np/search?component=&q= 검색어 &channel=user
# 쿠팡 상세링크 :https://www.coupang.com/np/search?q= 상품명 &channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=23&rocketAll=false&searchIndexingToken=&backgroundColor=
def get_search_link(word):
    # 검색어에 맞게 해당 링크를 bs4로 반환함
    address = req.get("https://www.coupang.com/np/search?component=&q="+str(word)+"&channel=user")
    address.raise_for_status()
    soup = bfu(address.text, 'html.parser')
    return soup

def get_productnumber(product):
    #해당 상품에 총 갯수를 알려주는 함수로 int형으로 반환 함
    soup = get_search_link(str(product))