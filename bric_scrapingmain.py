import bric_scraping as bric

# 브릭 대학원생 채용 정보 사이트에서 내가 원하느 정보만 필터링해서 보고 싶어서 만든 코드

find_word =["생명공학","시스템","컴퓨터","정보","합성",]
start=1
bric.print_filtering_find_number(find_word,start)
print("종료되었습니다.")