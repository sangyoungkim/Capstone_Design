from ast import Num
from asyncio.windows_events import NULL
import requests as req
from bs4 import BeautifulSoup as bfu
import re



# 19성인 웹툰은 셀렉터 조건이 달라서 회차 가져오기에서 오류가남



main_address = req.get("https://comic.naver.com/webtoon/weekday")
main_address.raise_for_status()
#제대로 가져왔는지 오류 검증코드 오류시 프로그램 강제 중단
main_soup = bfu(main_address.text,'html.parser')
#start_soup에 가져온 코드 html 코드 텍스트 형식으로 넣어줌

# 2차원 배열에 웹툰 이름과 이름 넣기
#이름 넣기

#main_soup.select_one('.list_area .col:nth-child(요일넘버) ul li:nth-child(웹툰넘버)').get_text().strip()

def innum_putday(num):
    if(num == 1):
        return "월요일"
    elif(num == 2):
        return "화요일"
    elif(num == 3):
        return "수요일"
    elif(num == 4):
        return "목요일"
    elif(num == 5):
        return "금요일"
    elif(num == 6):
        return "토요일"
    elif(num == 7):
        return "일요일"
    else:
        return NULL
        

def popular_rank(): #웹툰 인가 순위 탑 10을 확인합니다.
    print("======웹툰 랭크입니다.======")
    for i in range(1,10):
        rank = "rank0"+str(i)
        print(i,"위 :",main_soup.find("li",attrs={"class":rank}).a.get_text())
    
    print("10위 :",main_soup.find("li",attrs={"class":"rank10"}).a.get_text())
    print(" ")

def retrun_dailycartoon(i):
    #i가 반환받을 요일 1= 월요일 2=화요일 3=수요일 .... 등
    box=[]
    j=1
    while(main_soup.select_one('.list_area .col:nth-child('+str(i)+') ul li:nth-child('+str(j)+')>a'))!=None:
        box.append(main_soup.select_one('.list_area .col:nth-child('+str(i)+') ul li:nth-child('+str(j)+')>a ').get_text().strip())
        j=j+1
    return box  #배열로 반환함

def retrun_linkcartoon(i):
    #i가 반환받을 요일 1= 월요일 2=화요일 3=수요일 .... 등
    box=[]
    j=1
    while(main_soup.select_one('.list_area .col:nth-child('+str(i)+') ul li:nth-child('+str(j)+')>a'))!=None:
        box.append("https://comic.naver.com"+main_soup.select_one('.list_area .col:nth-child('+str(i)+') ul li:nth-child('+str(j)+')>a ').get('href'))
        j=j+1
    return box  #배열로 반환함

def get_linkopen(link,num):
    #링크를 입력하면 해당 링크의 웹툰 num회차 링크얻기
    address = req.get(str(link))
    address.raise_for_status()
    soup = bfu(address.text,'html.parser')

    link = link.replace('list','detail') # list 문자 찾아서 detail로 치환
    indext = link.find("&") + 1 #인덱스에 &문자+1 위치 찾아서 넣어줌 
    link = link[:indext] + "no="+str(num)+"&" + link[indext:] #찾은 인덱스값 사이에 해당 문자 넣어줌
    return link

def get_lastround(link,value):
    #매개변수로 입력받은 해당 링크에 웹툰 마지막 회차수 얻음 value 값이 참이면 링크 반환 거짓이면 회차 받환 value값 boolean 아니면 중단
    if(type(value) != bool):
        print("error: 잘못된 value 입니다")
        return NULL
    else:
        address = req.get(str(link))
        address.raise_for_status()
        #제대로 가져왔는지 오류 검증코드 오류시 프로그램 강제 중단
        soup = bfu(address.text,'html.parser')

        if(soup.find("tr",attrs={"class":"band_banner v2"}) != None):
            link = "https://comic.naver.com" + (soup.find("tr",attrs={"class":"band_banner v2"}).next_sibling.next_sibling).a.get('href')
            #컷툰의 경우 오류 나니깐 table viewList 로 바꾸고 자식 node 찾아가야함 -->밥먹고 ㄱ
            if(value == True):
                return link
            else:
                return link[link.find("no=")+3:link.find("&w")] # 문자열 슬라이싱
        
        else:
            link = "https://comic.naver.com"+soup.find("table",attrs={"class":"viewList"}).a.get('href')
            if(value == True):
                return link
            else:
                return link[link.find("no=")+3:link.find("&w")] # 문자열 슬라이싱

# #오류 왜? 아래 방식대로 오류 해결해서 사용하면 next_sibling 없이 가능해서 휴재만화인 경우 오류나는 if없이 가능 더효율적
# def get_lastround(link,value):
#     #매개변수로 입력받은 해당 링크에 웹툰 마지막 회차수 얻음 value 값이 참이면 마지막회차 링크도 받환 value값 boolean 아니면 중단
#     if(type(value) != bool):
#         print("error: 잘못된 value 입니다")
#         return NULL
#     else:
#         address = req.get(str(link))
#         address.raise_for_status()
#         #제대로 가져왔는지 오류 검증코드 오류시 프로그램 강제 중단
#         soup = bfu(address.text,'html.parser')
#         print(soup.select_one('#content table tbody'))
#     #//*[@id="content"]/table/tbody/tr[3]/td[2]/a
# print(get_lastround("https://comic.naver.com/webtoon/list?titleId=758037&weekday=mon",True))


def get_title(link):
    #링크를 통해서 변수 받아서 그 링크만화에 제목 가져오는 거지만 ! 링크를 제대로 안주면 오류
    address = req.get(str(link))
    address.raise_for_status()
    #제대로 가져왔는지 오류 검증코드 오류시 프로그램 강제 중단
    soup = bfu(address.text,'html.parser')
    title =(soup.select_one('#sectionContWide .tit_area .view').get_text())
    return (title[ :title.find("이전화")]).strip()


def get_img(link):
    img_address = req.get(link)
    img_address.raise_for_status()
    img_soup=bfu(img_address.text,"html.parser")

    i = 1
    while(True):
        if img_soup.select_one("#comic_view_area .wt_viewer img:nth-child("+str(i)+")") == None:
            break
        cartoon_img = req.get(str(img_soup.select_one("#comic_view_area .wt_viewer img:nth-child("+str(i)+")")['src'])) #이미지 링크 가져옴
        cartoon_img.raise_for_status()
        with open(str(get_title(link))+"{}.jpg".format(i),"wb") as f: #파일 오픈 해서 겟타이틀로 해당제목 가져와서 그 제목으로 파일명 정함
            f.write(cartoon_img.content) #이미지 파일 저장 
        i=i+1
