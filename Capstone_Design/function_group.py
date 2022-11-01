import re,json
from datetime import datetime 
import urllib.request as req
from bs4 import BeautifulSoup as bfu
import requests as requ
import pandas as pd
import numpy as np

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

def keyword_stock_news_naver_2(keyword,time_range = True,news_num=3):
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
            while(len(box_arr)<int(news_num) and len(stock[i]) != 0 ):
                if(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area") == None): 
                    break
                if(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area").get_text().find(str(j)) == -1): 
                    break
                else:
                    box_arr.append(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_tit").get_text() + " = " + soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area>a").attrs['href'])
                    num = num +1
            box_arr = list(set(box_arr))
            box_dic[j] = box_arr
            if(len(box_arr) >= int(news_num)-1):
                dic[i] = box_dic
                box_dic = {}
                box_arr = []
    return dic

def get_stock_information(stock,year=2):
#입력한 주식 정보를 year전까지 정보 가져와서 보여줍니다.
#출처는 네이버 증권입니다.
    # 주식 코드 찾아서 stockcode에 넣음
    link = requ.get("https://mweb-api.stockplus.com/api/search/assets.json?keyword="+str(stock))
    link.raise_for_status()
    json_file = json.loads(str(bfu(link.text, 'html.parser')))
    while(True):
        if json_file['assets']:
            stockcode = str(json_file['assets'][0]['code']).replace("A","")
            break
        else:
            print("정확한 주식명을 입력하세요")
            return None

    # 주식코드 넣어서 해당 주식 정보가져옴
    now = datetime.now()
    endtime = str(now).replace("-","").split(" ")[0]
    starttime = starttime = str(int(now.year) - int(year))+str(now.month)+str(now.day)
    stock_information_link = \
    "https://api.finance.naver.com/siseJson.naver?symbol="\
    +str(stockcode)+"&requestType=1&startTime="+starttime+"&endTime="+endtime+"&timeframe=day"
    link = requ.get(stock_information_link)
    link.raise_for_status()
    soup = bfu(link.text, 'lxml')
    df = soup.select_one("body").get_text().replace('"',"").replace("\n","").replace("\t","").replace(" ","").replace("[","").replace("]","").replace("'","")
    arr = np.array([])
    box = ""
    for i in df:
        if (i == ","):
            arr = np.append(arr,box)
            box = ""
        else:
            box += i
    arr = np.append(arr,df[-5::1])
    arr = arr.reshape(-1,7)
    df = pd.DataFrame(arr)
    df = df.drop(columns=[5,6], axis=1) #거래량 외국인 소진율 삭제
    df = df.drop(index=0, axis=0)
    df.columns = ['날짜', '시가', '고가', '저가', '종가']
    
    return df
a = get_stock_information("삼성전자")
print(a)

#====================================================================

user = ['삼성전자','용평리조트']
#1. 깃 깃허브 사용
#2. 상영 코드 설명
#3. 프론트 ui로 속도 느리거 덮는거 의논
#4. 진이 전달

#최종 진우형이 코드 이어서 작성

# 진이는 프론트 디자인 설계 끝나는대로 백 연동법 의논 상의