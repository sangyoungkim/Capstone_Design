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


#====================================================================

#1. 깃 깃허브 사용
#2. 상영 코드 설명
#3. 프론트 ui로 속도 느리거 덮는거 의논
#4. 진이 전달

#최종 진우형이 코드 이어서 작성

# 진이는 프론트 디자인 설계 끝나는대로 백 연동법 의논 상의

#====================================================================
# 주식 분석

import matplotlib.pyplot as plt 
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error 

get_df = get_stock_information("램테크놀러지",3)
stock_df = get_df.astype(int) # obj -> int
stock_df = stock_df.rename(columns={'날짜':'Date','시가':'Open', '고가':'High', '저가':'Low', '종가':'Close'})
print(stock_df.info())

# 이동평균선
stock_df['5'] = stock_df['Close'].rolling(5).mean()
stock_df['20'] = stock_df['Close'].rolling(20).mean()
stock_df['60'] = stock_df['Close'].rolling(60).mean()
stock_df['120'] = stock_df['Close'].rolling(120).mean()

plt.figure(figsize=(10,7))
plt.plot(stock_df.index,stock_df['Close'],',')
plt.plot(stock_df['5'], label='5')
plt.plot(stock_df['20'],label='20')
plt.plot(stock_df['60'],label='60')
plt.plot(stock_df['120'],label='120')
plt.xlabel('DATE')
plt.ylabel('Close Price')
plt.legend()

plt.show

# 이동평균선 보고 상승세 파악
if stock_df['5'].iloc[-1]<stock_df['20'].iloc[-1] and stock_df['20'].iloc[-1]<stock_df['60'].iloc[-1] and stock_df['60'].iloc[-1]<stock_df['120'].iloc[-1]:
    print("상승세")
else:
    print("크게 추천하지 않음")

# SVM으로 다음날 주식 가격 예측
stock_df_td = stock_df.tail(200) # 최근200일정도만 training
# print(stock_df_td)
# print(stock_df.info())

# stock_df_train = stock_df.tail(len(stock_df_td)-1) # 확인용
stock_df_close = stock_df_td['Close']
stock_df_close = stock_df_close.values

days=[]
for i in range(1,len(stock_df_td)+1):
    days.append([int(i)])

# training
rbf_svr = SVR(kernel='rbf', C=10000, gamma=0.0001)
rbf_svr.fit(days,stock_df_close)

lin_svr = SVR(kernel="linear", C=10000)
lin_svr.fit(days,stock_df_close)

poly_svr = SVR(kernel="poly", C=10000, degree=2)
poly_svr.fit(days,stock_df_close)

# predict
day = [[len(days)+1]]
print("RBF SVR 예측가격:",rbf_svr.predict(day))
print("Linear SVR 예측가격:",lin_svr.predict(day))
print("Poly SVR 예측가격:",poly_svr.predict(day))

pred_price = []
for i in range(len(days)):
    pred_price.append(rbf_svr.predict([[i]]))

plt.figure(figsize=(10,7))
plt.plot(stock_df_td.index,stock_df_td['Close'])
plt.plot(pred_price,'o')
# plt.plot(sam_df['20'],label='20')
# plt.plot(sam_df['60'],label='60')
# plt.plot(sam_df['120'],label='120')
plt.xlabel('DATE')
plt.ylabel('Close Price')
plt.legend()

plt.show
# %%
