import function_group as func

RT_search_text = func.RT_search_text()
stock_dic = func.RT_search_stock(RT_search_text)
# a = func.keyword_stock_news_plus(RT_search_text)
# for i in RT_search_text:
#     print(i)
#     print(stock_dic[i])
#     for j in a:
#         if(str(j) == str(i)):
#             print(a[j])
#     print("=====================")
a = func.keyword_stock_news_naver(RT_search_text)
for i in a :
    print(i,": ",end='')
    for j in a[i]:
        print(",",j,end='')
    print("")