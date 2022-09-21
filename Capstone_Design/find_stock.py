#증권플러스에서 실시간 검색에 키워드에 따른 주식관련 기사 스크래핑 
#Json 스크래핑 구조이지만 josn 요청이 안되서 텍스트 형식으로 가져와서 다룰 예정
import RT_search_text as RT
import requests as req
from bs4 import BeautifulSoup as bfu
import re, json

# 딕셔너리 안에 있는 값 가독성 높여서 출력
def print_dic(dic):
    for i in dic:
        print(i+" : ",end="")
        for j in range(0,len(dic[i])):
            print(dic[i][j]+"  ",end="")
        print("")

# 실시간 검색어에 맞게 주식 찾아서 담는 코드==================================
RT_keyword_news_dic = {} # 실시간 검색어에 키워드에 따른 관련 주식 담을 딕셔너리
stock_site_link = "https://mweb-api.stockplus.com/api/search/news_related_assets.json?keyword="
for i in range(1,11):
    address = req.get(re.sub(" ","%20",stock_site_link + str(RT.RT_keyword[i]) + "&limit=5"))
    address.raise_for_status()
    soup = bfu(address.text, 'html.parser')
    json_infomation = json.loads(str(soup))
    box = []
    for j in range(0,len(json_infomation["newsRelatedAssets"])):
        box.append(json_infomation["newsRelatedAssets"][j]["name"])
    RT_keyword_news_dic[str(RT.RT_keyword[i])] = box
# 실시간 검색어에 맞게 주식 찾아서 담는 코드=================================

print_dic(RT_keyword_news_dic)
# 해당 추천 주식이 실시간 검색어와 관련이 있는 뉴스 링크만 남기는 코드========

# 주식이 해당 실시간 검색어와 관련성이 있는지 검사하는 코드짜야함.

#키워드하고 상장 기업 네이버에 치고 유효한 기사로 판단할까? 
#유효 기준은? 기사 올라온 시간? 두단어가 다 있는거?
# T F 으로 반환할거면 해당에 맞는 함수를 짜는게 좋을까?