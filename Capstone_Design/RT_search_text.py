# Real Time search news text scraype 
# 기준 사이트 시그널실시간 Json 스크래핑 구조
import urllib.request as req
import json, datetime

signal_RT_search = req.urlopen("https://api.signal.bz/news/realtime")
RT_search_json = json.load(signal_RT_search)
RT_keyword = [datetime.datetime.now()] 
RT_news = [datetime.datetime.now()] 
# 실시간 검색어를 저장할 배열 첫번째 값에 실시간 검색어 스크래핑할 현재 시간 적용
for i in range(0,10):
    RT_keyword.append(RT_search_json['top10'][i]['keyword'])
    RT_news.append(RT_search_json['articles'][i]['title'])
# 배열에 실시간 검색어 10개 넣음
