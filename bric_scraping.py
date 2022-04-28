import requests as req
from bs4 import BeautifulSoup as bfu

address = req.get("https://www.ibric.org/myboard/list.php?Board=job_recruit&selflevel=1") #브릭 대학원생 채용정보사이트
address.raise_for_status()
soup = bfu(address.text, 'html.parser')
#https://www.ibric.org/myboard/list.php?Board=job_recruit&Page=2&selflevel=1

def get_recruitment_contents_number():
    # "https://www.ibric.org/myboard/list.php?Board=job_recruit&selflevel=1"
    # 위 브릭 대학원생 채용 정보사이트에 채용공고물 갯수를 반환 무조건 해당 페이지 임으로 매개변수없음
    return int(soup.find('div',attrs={'align':'center'}).get_text())
    # 특정 class나 id가 없어서 find로 가장 첫번째로 찾아지는 채용공고에 넘버 값에 이용했음 페이지에서 ui변경시 달라짐


