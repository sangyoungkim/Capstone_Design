import requests as req
from bs4 import BeautifulSoup as bfu
import numpy
address = req.get("https://www.ibric.org/myboard/list.php?Board=job_recruit&selflevel=1") #브릭 대학원생 채용정보사이트
address.raise_for_status()
soup = bfu(address.text, 'html.parser')
#https://www.ibric.org/myboard/list.php?Board=job_recruit&Page=2&selflevel=1?

start = 11 # 몇페이지 부터 찾을지 너무많아서 일단 10값으로 설정 나중에 1로 상수 값으로 전환해야함

def get_recruitment_contents_number():
    #채용정보 총 갯수 반환
    # "https://www.ibric.org/myboard/list.php?Board=job_recruit&selflevel=1"
    # 위 브릭 대학원생 채용 정보사이트에 채용공고물 갯수를 반환 무조건 해당 페이지 임으로 매개변수없음
    return int(soup.find('div',attrs={'align':'center'}).get_text())
    # 특정 class나 id가 없어서 find로 가장 첫번째로 찾아지는 채용공고에 넘버 값에 이용했음 페이지에서 ui변경시 달라짐

def print_recruitment_contents_all():
    #채용정보 전부 프린팅
    #아래 주석은 채용정보 제목 가져오는 셀렉터
    #'body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
    #td table  tr:nth-child(2) td table  tr:nth-child(이 안에 값이 3부터 시작 2씩증가) td:nth-child(2) a')

    page_number=1
    while(True):
        a = req.get("https://ibric.org/myboard/list.php?Board=job_recruit&Page=" + str(
            page_number) + "&selflevel=1")  # 브릭 대학원생 채용정보사이트
        a.raise_for_status()
        s = bfu(a.text, 'html.parser')
        page_number = page_number + 1

        #아래 주석 : 마지막 페이지에서 다음 페이지로 넘기면 마지막 페이지가 나오는데 만약 마지막페이지하고 다음 페이지가 같은면
        #           마지막 페이지라고 판단해서 브레이크
        # a1 = req.get("https://ibric.org/myboard/list.php?Board=job_recruit&Page=" + str(
        #     page_number) + "&selflevel=1")  # 브릭 대학원생 채용정보사이트
        # a1.raise_for_status()
        # s1 = bfu(a1.text, 'html.parser')
        # if(s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
        #                 td table  tr:nth-child(2) td table  tr:nth-child(' + str(page_number) + ') td:nth-child(2) a') == \
        #         s1.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
        #                 td table  tr:nth-child(2) td table  tr:nth-child(' + str(page_number+1) + ') td:nth-child(2) a')):
        #     print("끝 ")
        #     break

        page_number = page_number + 1

        information_number = 3

        while(s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                        td table  tr:nth-child(2) td table  tr:nth-child(' + str(information_number) + ') td:nth-child(2) a') != None):
        # 더이상 값이 없을때 까지인데 그 값은 모집학과 정보로 판단
            number = s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                                td table  tr:nth-child(2) td table  tr:nth-child(' + str(information_number) + ') td:nth-child(1) div').get_text() # 모집 번호
            main_department = s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                                td table  tr:nth-child(2) td table  tr:nth-child(' + str(information_number) + ') td:nth-child(2) a').get_text() #모집학교학과 정보 저장
            degree =  s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                                td table  tr:nth-child(2) td table  tr:nth-child(' + str(information_number) + ') td:nth-child(4)').get_text() #모집 학위저장
            deadline =  s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                                td table  tr:nth-child(2) td table  tr:nth-child(' + str(information_number) + ') td:nth-child(5)').get_text() #모집 마감일 저장
            print(number,main_department,degree,deadline)
            information_number = information_number + 2 # 값이 2단위로 증가해야함 1씩 증가시 가운데 있는 다른 value값을 가져옴
        if(int(number) == 1): # 각 채용 정보마다 넘버가 있다. 마지막이 1번인데 그 1번에 도달하면 브레이크
            break ##

def filtering_find_number(arr):
    #arr로 받은 배열 안에 있는 단어가 있는 채용정보만 찾아서 리턴해줌
    # 라고 생각했지만 생각해보니 번호만 알면 정보 다 가져올 수 있네..?
    filtering_arr=[]
    page_number = start # 시작하고싶은 페이지 부터 번호 입력해주면 됨
    while(True):
        a = req.get("https://ibric.org/myboard/list.php?Board=job_recruit&Page=" + str(
            page_number) + "&selflevel=1")  # 브릭 대학원생 채용정보사이트
        a.raise_for_status()
        s = bfu(a.text, 'html.parser')
        information_number = 3 #찾고자하는 리스트들이 3부터 2씩증가함
        while (s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                               td table  tr:nth-child(2) td table  tr:nth-child(' + str(
            information_number) + ') td:nth-child(2) a') != None):
            number = s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                                           td table  tr:nth-child(2) td table  tr:nth-child(' + str(information_number) + ') \
                                           td:nth-child(1) div').get_text()  # 모집 번호
            main_department = s.select_one('body table:nth-child(2)  tr td:nth-child(1) table  tr:nth-child(2) td table  tr:nth-child(2)\
                                           td table  tr:nth-child(2) td table  tr:nth-child(' + str(information_number) + ') \
                                           td:nth-child(2) a').get_text()  # 모집학교학과 정보 저장 원하는 정보를 찾기위해 필요

            for i in range(0,len(arr)):
                if(main_department.find(str(arr[i])) != -1): # if 조건문 안에 값이 -1이 아닐시 찾은거 즉 모집문구에 원하는 해당 단어가 없을시
                    filtering_arr.append(number)
            information_number = information_number + 2

        if (int(number) == 1):  # 각 채용 정보마다 넘버가 있다. 마지막이 1번인데 그 1번에 도달하면 브레이크
            break
        page_number = page_number + 1
    return filtering_arr

def find_print(arr):
    #찾은 값들 프린트
    numlist = filtering_find_number(arr)
    print(numlist)


arr = ["공학","시스템","컴퓨터","정보","합성",]
find_print(arr)
