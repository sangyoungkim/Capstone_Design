import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
#X축 기간 Y축 랭크 각 상품이 기간에 따라 랭크가 어떻게 변하는지

# def fuc_1(arr):
#     #입력받은 데이터 프레임을 배열형태로 반환해주는 함수로 
#     #데이터 프레임에 특정 한개의 colums만 매개변수로 입력해야한다 
#     #또한 x축과 y축에 값으로 쓸 배열을 위한 함수로 배열내 중복값을 전부 제거해준ㄷ

#     arr = arr.values#데이터 프레임을 배열형식으로 변환 (2차원 배열)
#     rearr=[]
#     for i in range(0,len(arr)):
#         rearr.append(arr[i][0])
#     #2차원 배열을 1차원 배열로 변경해줌
#     rearr = set(rearr)

#     return rearr

main_data = pd.read_csv("datatest.csv")
plt.plot(main_data['date'],main_data['rank'],label='product_name')
plt.xlabel('date')
plt.ylabel('rank')
plt.show()
#데이터 프레임 활용해서 그래프 그리는 영상보고 하면될듯
