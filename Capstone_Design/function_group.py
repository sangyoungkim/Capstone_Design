import re, datetime,json
import urllib.request as req
from bs4 import BeautifulSoup as bfu
import requests as requ

def RT_search_text(text = True):
# 실검 배열로 반환, False시 뉴스 반환
    RT_keyword = [] # 실시간 검색어 담을 배열
    RT_news = [] # 실시간 뉴스 담을 배열
    RT_search_json = json.load(req.urlopen("https://api.signal.bz/news/realtime"))
    # 실시간 검색어를 저장할 배열 첫번째 값에 실시간 검색어 스크래핑할 현재 시간 적용
    for i in range(0,10):
        RT_keyword.append(RT_search_json['top10'][i]['keyword'])
        RT_news.append(RT_search_json['articles'][i]['title'])
    if(text):
        return RT_keyword
    else:
        return RT_news
def RT_search_stock(key_word):
    #실시간 검색어에 맞게 주식 찾아서 담아서 딕셔너리로 반환
    RT_keyword_news_dic = {}
    stock_site_link = "https://mweb-api.stockplus.com/api/search/news_related_assets.json?keyword="
    for i in range(0,10):
        address = requ.get(re.sub(" ","%20",stock_site_link + str(key_word[i]) + "&limit=5"))
        address.raise_for_status()
        soup = bfu(address.text, 'html.parser')
        json_infomation = json.loads(str(soup))
        box = []
        for j in range(0,len(json_infomation["newsRelatedAssets"])):
            box.append(json_infomation["newsRelatedAssets"][j]["name"])
        RT_keyword_news_dic[str(key_word[i])] = box
    return RT_keyword_news_dic
def keyword_stock_news_naver_2(keyword,time_range = True):
# 배열로 입력 받은 키워드에 맞는 뉴스를 가져와서 dic로 반환
# 실검과 증권플러스추천 주식 같이 검색해서 나오는 뉴스에서 주식키워드 찾는 방식
    dic = {}
    stock = RT_search_stock(keyword)
    if(time_range): time_range = 12
    else: time_range = 4
    for i in stock:
        box_dic = {}
        box_arr = []
        for j in stock[i]:
            word = str(i) + str(j)
            word.replace(" ","%")
            link = requ.get("https://search.naver.com/search.naver?where=news&query="+word+"&sm=tab_opt&sort=0&photo=0&field=0&pd="+str(time_range)+"&start=1")
            link.raise_for_status()
            soup = bfu(link.text, 'html.parser')
            num = 1
            while(len(box_arr)<3 and len(stock[i]) != 0 ):
                if(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area") == None): 
                    break
                if(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area").get_text().find(str(j)) == -1): 
                    break
                else:
                    box_arr.append(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_tit").get_text() + " = " + soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area>a").attrs['href'])
                    num = num +1
            box_dic[j] = box_arr
            if(len(box_arr) >= 2):
                dic[i] = box_dic
                box_dic = {}
                box_arr = []
    return dic

