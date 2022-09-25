#증권플러스에서 실시간 검색에 키워드에 따른 주식관련 기사 스크래핑 
#Json 스크래핑 구조이지만 josn 요청이 안되서 텍스트 형식으로 가져와서 다룰 예정
from types import NoneType
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

# 4.검색하면서 뉴스 링크 전부 가져옴 (기준 네이버)=============================
#fuction_group 에 있는 time 메소드 값 기준 안에 있는뉴스 기사만 가져옴
RT_keyword_news_dic = {} #값 초기화 하고 안에 키워드 : 링크로 담음.
for i in RT_search_keyword:
    for j in i:
        address = req.get(re.sub("검색어",str(j),search_link).replace(" ","%20"))
        address.raise_for_status()
        soup = bfu(address.text, 'html.parser')
        box = []
        for k in soup.select(".list_news .news_area .news_tit"):
            box.append(k['href'])
        if(len(box) != 0):
            RT_keyword_news_dic[j] = box
func.print_dic(RT_keyword_news_dic)
# 4.검색하면서 뉴스 링크 전부 가져옴 (기준 네이버)=============================

# 4.검색하면서 뉴스 링크 전부 가져옴 (기준 증권플러스)==========================
