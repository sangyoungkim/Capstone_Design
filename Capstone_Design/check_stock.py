#%%

import function_group as func
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error 

# 주식 불러오기
def get_stock(stock,year=3):
    get_df = func.get_stock_information(stock,year)
    stock_df = get_df.astype(int) # obj -> int
    stock_df = stock_df.rename(columns={'날짜':'Date','시가':'Open', '고가':'High', '저가':'Low', '종가':'Close'})
    return stock_df


# 이동평균선 분석
def recommended_stock(stock,y):
    stock_df = get_stock(stock,y)
    stock_df['5'] = stock_df['Close'].rolling(5).mean()
    stock_df['20'] = stock_df['Close'].rolling(20).mean()
    stock_df['60'] = stock_df['Close'].rolling(60).mean()
    stock_df['120'] = stock_df['Close'].rolling(120).mean()

    plt.figure(figsize=(10,7))
    plt.plot(stock_df.index,stock_df['Close'],',')
    plt.plot(stock_df['5'], label='5')
    plt.plot(stock_df['20'],label='20')
    plt.plot(stock_df['60'],label='60')
    plt.plot(stock_df['120'],label='120')
    plt.xlabel('DATE')
    plt.ylabel('Close Price')
    plt.legend()

    plt.show

    # 이동평균선 보고 상승세 파악
    if stock_df['5'].iloc[-1]<stock_df['20'].iloc[-1] and stock_df['20'].iloc[-1]<stock_df['60'].iloc[-1] and stock_df['60'].iloc[-1]<stock_df['120'].iloc[-1]:
        print("이동평균선 분석 결과 현재 주식이 상승세로 판단됩니다.")
    else:
        print("이동평균선 분석 결과 현재 주식을 크게 추천하지 않습니다.")
    

def predict_stock(stock,y):
    stock_df = get_stock(stock,y)
    # SVM으로 다음날 주식 가격 예측
    stock_df_td = stock_df.tail(200) # 최근200일정도만 training

    # stock_df_train = stock_df.tail(len(stock_df_td)-1) # 확인용 (개발자 외 사용금지)
    stock_df_close = stock_df_td['Close']
    stock_df_close = stock_df_close.values

    days=[]
    for i in range(1,len(stock_df_td)+1):
        days.append([int(i)])

    # training
    rbf_svr = SVR(kernel='rbf', C=10000, gamma=0.0001)
    rbf_svr.fit(days,stock_df_close)

    lin_svr = SVR(kernel="linear", C=10000)
    lin_svr.fit(days,stock_df_close)

    poly_svr = SVR(kernel="poly", C=10000, degree=2)
    poly_svr.fit(days,stock_df_close)

    # predict
    day = [[len(days)+1]]
    print("RBF SVR 예측가격:",rbf_svr.predict(day)) # 성능 가장 좋음
    print("Linear SVR 예측가격:",lin_svr.predict(day))
    print("Poly SVR 예측가격:",poly_svr.predict(day))

    # 예측 그래프

    # pred_price = []
    # for i in range(len(days)):
    #     pred_price.append(rbf_svr.predict([[i]]))

    # plt.figure(figsize=(8,5))
    # plt.plot(stock_df_td.index,stock_df_td['Close'])
    # plt.plot(pred_price,'o')
    # # plt.plot(sam_df['20'],label='20')
    # # plt.plot(sam_df['60'],label='60')
    # # plt.plot(sam_df['120'],label='120')
    # plt.xlabel('DATE')
    # plt.ylabel('Close Price')
    # plt.legend()

    # plt.show
# %%
