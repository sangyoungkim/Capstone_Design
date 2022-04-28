import cartoon_scraping as prc

dic_cartoon = {}
cartooon_name = []
cartoon_link = []
user = 0
# 위 배열 딕셔너리에 다 각각 값 넣어주는 구문


print("========================= 네이버 웹툰 스크래핑 공부 =========================")
while (user != -1):
    user = int(input("1. 웹툰 랭킹 보기 2. 요일별 웹툰보기 (-1입력시 종료)"))
    if (user == -1):
        print('종료 됩니다.')
        break
    elif (user == 1):
        print("=========실시간 랭킹입니다.=========")
        prc.popular_rank()
    elif (user == 2):
        user = int(input("1.월 2.화 3.수 4.목 5.금 6.토 7.일 "))
        if (user == -1):
            print('종료 됩니다.')
            break
        print(prc.innum_putday(user) + "입니다.")

        # 요일에 맞게 변수에 넣어주는 구문
        cartoon_name = prc.retrun_dailycartoon(user)
        cartoon_link = prc.retrun_linkcartoon(user)
        for i in range(0, len(cartoon_name)):
            dic_cartoon[cartoon_name[i]] = cartoon_link[i]

        print("")
        # 해당 요일 출력하는 구문
        i = 0
        for k, v in dic_cartoon.items():
            i = i + 1
            print(str(i) + ". 제목 : {0:<25}".format(k) + "링크 : {0:<25}".format(v))
        iuser = int(input("웹툰 보러 가기 원할시 번호를 입력해주세요 (없는 번호 입력시 초기화면)"))
        if (0 < user <= len(cartoon_link)):
            print("1화 ~ " + prc.get_lastround(cartoon_link[iuser - 1], False) + "화")
            user = int(input("입력하신 회차로 이동합니다. 회차를 입력해주세요(없는 번호 입력시 초기화면)"))
            colink = cartoon_link[iuser - 1]
            if (1 <= user <= int(prc.get_lastround(cartoon_link[iuser - 1], False))):
                print(user, "화 제목 : ", prc.get_title(prc.get_linkopen(colink, user)))
                print("보러가기 링크 : ", prc.get_linkopen(colink, user))

        else:
            print("숫자 입력이 잘못됬습니다.")

