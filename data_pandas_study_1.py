
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
#문제 : data.csv 모든 기간동안 입력 받은 순위 이상을 항상 유지한 상품 시각화 해서 반환

user_number = int(input("입력하신 순위 이상을 유지한 상품을 시각화 합니다 (100이상의 숫자만 입력): "))

#=======================데이터 프레임 가져와서 원하는 정보만 남겨서 저장
main_data = pd.read_csv("datatest.csv") # 데이터프레임 형태로 파일 가져옴
df = pd.DataFrame(main_data,columns=['rank','product_name','date'],index=range(700))
#메인 데이터에서 필요한 컬럼만 가져와서 저장함. 인덱스 지정해줌(인덱스 지정은 데이터 가공편의를 위해서 함)

#=======================상품이름 배열로 저장하기
name_df =  pd.DataFrame(df,columns=['product_name']) 
#데이퍼 프레임 네임에 있는 애들 전부 가져와서 저장함 (중복값 있음)
name_np = name_df.to_numpy() #데이터 프레임을 넌파이 형식 배열 (2차원 배열로 바꿔줌)

name_arr = [] # 중복을 제거한 상품이름만 넣어서 저장할 배열임
for i in range(700):
    name_arr.append(name_np[i][0])
#numpy형식 2차원 배열을 다루기 쉬운 1차원 배열형태로 저장해줌
#여기까지 시행시 name_arr에 상품명이 리스트로 저장되어 들어감

#=======================중복 제거과정
#분명 배열 중복 제거해주는 함수가 있겠지만 알고리즘 공부를 위해 직접짠다.
def delete_overlap(arr): #중복제거해주는 함수
    unoverlap_arr=[]
    judgment = True
    for i in arr:
        for j in unoverlap_arr:
            if i == j:
                judgment = False
                break
            else:
                judgment = True
        if judgment:
            unoverlap_arr.append(i)
    return unoverlap_arr

sort_name_arr = delete_overlap(name_arr)
