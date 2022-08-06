
from itertools import count
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
#문제 : data.csv 모든 기간동안 입력 받은 순위 이상을 항상 유지한 상품 시각화 해서 반환

filtering_number =99 #int(input("입력하신 순위 이상을 유지한 상품을 시각화 합니다 (100이상의 숫자만 입력): "))

#=======================데이터 프레임 가져와서 원하는 정보만 남겨서 저장
main_data = pd.read_csv("datatest.csv") # 데이터프레임 형태로 파일 가져옴
df = pd.DataFrame(main_data,columns=['rank','product_name','date'],index=range(700))
#데이터가 700개인걸 아는 가정에서 가능한 코드
#메인 데이터에서 필요한 컬럼만 가져와서 저장함. 인덱스 지정해줌(인덱스 지정은 데이터 가공편의를 위해서 함)

#=======================상품이름하고 랭크만 남겨서 저장하는 과정.
#각회차마다 몇위였는지 저장하기 위해서 2차원 배열을 이용하는게 좋을거같음
arr_df =  pd.DataFrame(df,columns=['rank','product_name']) #랭크하고 이름만 데이터 프레임으로 가져옴
arr_df = arr_df.to_numpy() #배열로 바꿔줌 #2차원 배열형태로 랭크 이름 순으로 들어가 있음

#=======================입력받은 랭크조건에 총족하는 값들을 새로운 2차원 배열에 담는 과정.
filter_arr=[] # 조건에 맞는 랭크 이상값만 담음
for i in range(len(arr_df)):
    if(arr_df[i][0] <= filtering_number):
        filter_arr.append(arr_df[i][1])

#=======================이제 7번중복되는 애들만 남겨야함 총 데이터가 700개임을 알고 가능한 코드
def delete_overlap(arr): # 2차원배열 중복제거해주는 함수
    unoverlap_arr=[]
    judgment = True
    for i in arr:
        for j in unoverlap_arr:
            if i[1] == j[1]:
                judgment = False
                break
            else:
                judgment = True
        if judgment:
            unoverlap_arr.append(i)
    return unoverlap_arr

compare_arr = delete_overlap(filter_arr) # filter_arr에서 중복 제거한것.
#=======================중복제거한 배열을 순회하면서 값이 7개 미만인건 삭제 시키면 남은값이 최종결과.
result = []
for i in compare_arr:
    if(filter_arr.count(i) >= 7):
        result.append(i)

print(result)