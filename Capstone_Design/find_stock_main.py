import function_group as func

RT_search_text = func.RT_search_text()
stock_dic = func.RT_search_stock(RT_search_text)
a = func.keyword_stock_news(RT_search_text)
for i in RT_search_text:
    print(i)
    print(stock_dic[i])
    for j in a:
        if(str(j) == str(i)):
            print(a[j])
    print("=====================")