
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
#정문제 : data.csv X축 기간 Y축 랭크 각 상품이 기간에 따라 랭크가 어떻게 변하는지

#1. 받은 데이터에서 필요한 날짜 이름 랭크정보만 남겨서 가공
#2. 데이터 안에서 상품 이름만 가져와서 배열로 저장
#3. 배열안에 전체 이름 데이터가 있으므로 중복제거 과정이 필요함
#4. 이름으로 데이터 조회해서 그 상품에 날짜별 랭크를 얻어냄
#5. 배열 안에 있는 모든 상품 그래프 그려냄

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

name_arr = delete_overlap(name_arr)


# print(df[(df['product_name'] == name_arr[0])]) #0번째 인덱스값 프린트로 순위변화를 텍스트로 알려줌
# boxdf = df[(df['product_name'] == name_arr[0])]#df 에서 i와 같은 값만 가져와서 boxdf에 넣음
# plt.plot(boxdf['date'],boxdf['rank'])
#=======================그래프를 그림
for i in name_arr:
    boxdf = df[(df['product_name'] == i)]#df 에서 i와 같은 값만 가져와서 boxdf에 넣음
    plt.plot(boxdf['date'],boxdf['rank'])
#배열안에 저장되어있는 이름으로 값을 가져와서 배열의 길이의 데이터를 그래프를 중복해서 그려줌

plt.title("DATA SORTING HW")
plt.xlabel('date') # x축 이름 설정
plt.ylabel('rank')# y축 이름 설정
plt.grid(True)#눈금서 그림
plt.gca().invert_yaxis()
plt.show()# 그래프 보여줌
