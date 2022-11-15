import get_stock_info as func

RT_search_text = func.RT_search_text()
stock_dic = func.RT_search_stock(RT_search_text)

a = func.keyword_stock_news_naver(RT_search_text,False,4)
for i in a:
    print("실검:",i)
    for j in a[i]:
        print("주식:",j)
        print("<관련기사>")
        for k in a[i][j]:
            print(k)
    print("")