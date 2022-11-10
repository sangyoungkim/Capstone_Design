#%%
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
        if(address.status_code == 200):
            soup = bfu(address.text, 'html.parser')
            json_infomation = json.loads(str(soup))
            box = []
            for j in range(0,len(json_infomation["newsRelatedAssets"])):
                box.append(json_infomation["newsRelatedAssets"][j]["name"])
            RT_keyword_news_dic[str(key_word[i])] = box
        else:
            pass
    return RT_keyword_news_dic

def keyword_stock_news_naver(keyword,time_range = True,min_news_num=3,max_new_num=8):
# 배열로 입력 받은 키워드에 맞는 뉴스를 가져와서 dic로 반환
# 실검과 증권플러스추천 주식 같이 검색해서 나오는 뉴스에서 주식키워드 찾는 방식
    RT_arr = []
    stock_arr = []
    news_info = []
    stock = RT_search_stock(keyword)
    if(time_range): time_range = 12
    else: time_range = 4
    for RT in stock:
        box1_arr = []
        box3_arr = []
        for RT_stock in stock[RT]:
            if(len(stock[RT]) != 0):
                word = str(RT) +" " +str(RT_stock)
                word.replace(" ","%")
                link = requ.get("https://search.naver.com/search.naver?where=news&query="+word+"&sm=tab_opt&sort=0&photo=0&field=0&pd="+str(time_range)+"&start=1")
                link.raise_for_status()
                soup = bfu(link.text, 'html.parser')
                num = 1
                box_dic = {}
                box2_arr = []
                a = 0
                while(a<int(max_new_num)):
                    if(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area") == None): 
                        break #검색시 기사가 없으면
                    if(soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area").get_text().find(str(RT_stock)) != -1): 
                        box_dic["제목"] = soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_tit").get_text()
                        box_dic["내용"] = soup.select_one(".list_news .bx:nth-child("+str(num)+") .dsc_wrap").get_text()
                        box_dic["링크"] = soup.select_one(".list_news .bx:nth-child("+str(num)+") .news_area>a").attrs['href']
                        if(soup.select_one(".list_news .bx:nth-child("+str(num)+") a>img") == None): box_dic["사진"+str(num)] = None
                        else : box_dic["사진"] = soup.select_one(".list_news .bx:nth-child("+str(num)+") a>img").attrs['src']
                        a = a + 1
                    num = num + 1
                    box2_arr.append(box_dic)
                    box_dic = {}
                if(a >= int(min_news_num)):
                    if (RT not in RT_arr):RT_arr.append(RT)
                    box3_arr.append(box2_arr)
                    box2_arr = []
                    box_dic = {}
                    box1_arr.append(RT_stock)
                a = 0
                num = 1
        if(len(box3_arr)>0):news_info.append(box3_arr)
        if(box1_arr not in stock_arr and len(box1_arr) > 0 ):stock_arr.append(box1_arr)
    return RT_arr , stock_arr , news_info
            
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
    df = df.drop(columns=[5,6], axis=1) #거래량, 외국인 소진율 삭제
    df = df.drop(index=0, axis=0)
    df.columns = ['날짜', '시가', '고가', '저가', '종가']
    
    return df
a,b,c = keyword_stock_news_naver(RT_search_text(),True,2,3)
print(a)
print("==================")
print(b)
print("==================")
for i in c:
    print(i)
    print("-------------------")
# %%