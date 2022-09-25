import re, datetime,json
import urllib.request as req

# Real Time search and news text scraype ================================
# 기준 사이트 시그널실시간 Json 스크래핑 구조
RT_keyword = [datetime.datetime.now()] # 실시간 검색어 담을 배열
RT_news = [datetime.datetime.now()] # 실시간 뉴스 담을 배열
signal_RT_search = req.urlopen("https://api.signal.bz/news/realtime")
RT_search_json = json.load(signal_RT_search)
# 실시간 검색어를 저장할 배열 첫번째 값에 실시간 검색어 스크래핑할 현재 시간 적용
for i in range(0,10):
    RT_keyword.append(RT_search_json['top10'][i]['keyword'])
    RT_news.append(RT_search_json['articles'][i]['title'])
# 배열에 실시간 검색어 10개 넣음

# 딕셔너리 안에 있는 값 가독성 높여서 출력==============================
def print_dic(dic):
    for i in dic:
        print(i+" : ",end="")
        for j in range(0,len(dic[i])):
            print(dic[i][j]+"  ",end="")
        print("")

# 뉴스기사 검색에 이용될 범위시간과 현시간 배열로 반환====================
def input_time():
    date_range = 1 # 해당 변수 안에 값이 뉴스범위 ex) 2이면 2일전 뉴스까지만 보여줌
    t = str(datetime.datetime.now()).split(".")[0]
    t = t.replace("-",".").replace(" ",".").replace(":",".")
    t = t.split("."+t.split(".")[-1])[0]
    time = [re.sub(t.split(".")[3],str(int(t.split(".")[3])-date_range),t),t]
    return time