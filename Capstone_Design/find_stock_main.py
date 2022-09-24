#증권플러스에서 실시간 검색에 키워드에 따른 주식관련 기사 스크래핑 
#Json 스크래핑 구조이지만 josn 요청이 안되서 텍스트 형식으로 가져와서 다룰 예정
import requests as req
from bs4 import BeautifulSoup as bfu
import re, json
import fuction_group as func

RT_keyword_news_dic = {} # 실시간 검색어에 키워드에 따른 관련 주식 담을 딕셔너리.
RT_search_keyword =[] # 검색해서 뉴스 찾을 키워드 2차원 배열로 저장.

# 1.실시간 검색어에 맞게 주식 찾아서 담는 코드==================================
stock_site_link = "https://mweb-api.stockplus.com/api/search/news_related_assets.json?keyword="
for i in range(1,11):
    address = req.get(re.sub(" ","%20",stock_site_link + str(func.RT_keyword[i]) + "&limit=5"))
    address.raise_for_status()
    soup = bfu(address.text, 'html.parser')
    json_infomation = json.loads(str(soup))
    box = []
    for j in range(0,len(json_infomation["newsRelatedAssets"])):
        box.append(json_infomation["newsRelatedAssets"][j]["name"])
    RT_keyword_news_dic[str(func.RT_keyword[i])] = box
# 1.실시간 검색어에 맞게 주식 찾아서 담는 코드=================================

# 2.딕셔너리 안에 값 이용해서 검색어 만듬======================================
for j in RT_keyword_news_dic:
    box = []
    for i in RT_keyword_news_dic[j]:
        box.append(j+" "+i)
    RT_search_keyword.append(box)
# 2.딕셔너리 안에 값 이용해서 검색어 만듬======================================

# 3.검색할 네이버 사이트 검색링크 규격 만들기==================================
# 1일이전 뉴스만 정리하기 위해 날짜를 만들어서 넣어줘야함.
time = func.input_time()
search_link = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=검색어&sort=0&photo=0&field=0\
               &pd=4&ds=%s&de=%s&cluster_rank=31&mynews=0&office\
               _type=0&office_section_code=0&news_office_checked=&nso=so:r,p:1d,a:all&start=0"%(time[0],time[1])
search_link = re.sub(" ","",search_link)
# 3.검색할 네이버 사이트 검색링크 규격 만들기==================================

# 4.검색하면서 뉴스 링크 전부 가져옴 ==========================================
        



# 해당 추천 주식이 실시간 검색어와 관련이 있는 뉴스 링크만 남기는 코드========


# 해당 추천 주식이 실시간 검색어와 관련이 있는 뉴스 링크만 남기는 코드========
# 주식이 해당 실시간 검색어와 관련성이 있는지 검사하는 코드짜야함.

#키워드하고 상장 기업 네이버에 치고 유효한 기사로 판단할까? 
#유효 기준은? 기사 올라온 시간? 두단어가 다 있는거?
# T F 으로 반환할거면 해당에 맞는 함수를 짜는게 좋을까?