import re, datetime,json
import urllib.request as req
from bs4 import BeautifulSoup as bfu
import requests as requ

def RT_search_text(user = 1):
# 1. 실검 배열로 반환, 1이외 다른 값토픽 뉴스 반환
    RT_keyword = [] # 실시간 검색어 담을 배열
    RT_news = [] # 실시간 뉴스 담을 배열
    RT_search_json = json.load(req.urlopen("https://api.signal.bz/news/realtime"))
    # 실시간 검색어를 저장할 배열 첫번째 값에 실시간 검색어 스크래핑할 현재 시간 적용
    for i in range(0,10):
        RT_keyword.append(RT_search_json['top10'][i]['keyword'])
        RT_news.append(RT_search_json['articles'][i]['title'])
    if(int(user) == 1):
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

def keyword_stock_news(keyword):
# 배열로 입력 받은 키워드에 맞는 뉴스를 가져와서 dic로 반환
# 가장 높은 시간 복잡도(최적화 하려면..?)
    dic = {}
    for i in keyword:
       link = requ.get("https://mweb-api.stockplus.com/api/search/news.json?keyword=%s"%re.sub(" ","%20",str(i)))
       link.raise_for_status()
       json_file = json.loads(str(bfu(link.text, 'html.parser')))
       box = []
       for j in range(0,len(json_file['news'])):
        news_time = str(json_file['news'][j]['createdAt']).replace("T"," ").split(".")[0]
        news_time = datetime.datetime.strptime(news_time, '%Y-%m-%d %H:%M:%S').date()
        time = datetime.datetime.strptime(input_time(), '%Y-%m-%d %H:%M:%S').date() 
        if(str(news_time - time) == "0:00:00" or str(news_time - time) == "-1 day, 0:00:00"):
           # word = i.split(" ")
           # temp = False
           # for w in word:
           #     if(str(json_file['news'][j]['title']).find(str(w))!= -1):
           #         temp = True
           # if(temp):
           #     box.append(str(json_file['news'][j]['url']))
           box.append(str(json_file['news'][j]['url']))
        if(len(box) > 0): dic[i] = box
    return dic

def print_dic(dic):
# 딕셔너리 안에 있는 값 가독성 높여서 출력
    for i in dic:
        print(i+" : ",end="")
        for j in range(0,len(dic[i])):
            print(dic[i][j]+"  ",end="")
        print("")

def input_time():
# 현재 시간 반환
    return str(datetime.datetime.now()).split(".")[0]

