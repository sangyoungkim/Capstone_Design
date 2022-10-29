import function_group as func

RT_search_text = func.RT_search_text()
stock_dic = func.RT_search_stock(RT_search_text)

a = func.keyword_stock_news_naver_2(RT_search_text,False)
for i in a:
    print("실검:",i)
    for j in a[i]:
        print("주식:",j)
        print("<관련기사>")
        for k in a[i][j]:
            print(k)
    print("")