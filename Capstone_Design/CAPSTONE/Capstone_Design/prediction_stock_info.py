#%%
from Capstone_Design.get_stock_info import get_stock_information
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.svm import SVR
import os

# 주식 불러오기
def get_stock(stock,year=3):
    get_df = get_stock_information(stock,year)
    if get_df is None:
      return None
    else:
      stock_df = get_df.astype(int) # obj -> int
      stock_df = stock_df.rename(columns={'날짜':'Date','시가':'Open', '고가':'High', '저가':'Low', '종가':'Close'})
      return stock_df


# 이동평균선 분석 및 예측

def recommended_stock(stock,y):
    recom = 'none'
    rbf = 'none'
    cross = 'none'
    stock_df = get_stock(stock,3)

    if stock_df is None:
      return recom, rbf, cross
    else:
      stock_df['5'] = stock_df['Close'].rolling(5).mean()
      stock_df['20'] = stock_df['Close'].rolling(20).mean()
      stock_df['60'] = stock_df['Close'].rolling(60).mean()
      stock_df['120'] = stock_df['Close'].rolling(120).mean()

      a = np.arange(0,len(stock_df),len(stock_df)//5)

      label = stock_df.iloc[a,0]
      plt.figure(figsize=(10,7))
      # plt.plot(stock_df.index,stock_df['Close'],',')
      plt.plot(stock_df['5'], label='5',color='maroon')
      plt.plot(stock_df['20'],label='20',color='mediumorchid')
      plt.plot(stock_df['60'],label='60',color='dodgerblue')
      plt.plot(stock_df['120'],label='120',color='darkolivegreen')
      plt.xlabel('DATE')
      plt.ylabel('Close Price')
      plt.xticks(a,size=12,labels=label)
      plt.yticks(size=12)
      plt.legend()
      print('predict_stock_graph 완료')
      # plt.show
      plt.savefig('C:/Users/user/Desktop/CAPSTONE/CapstoneApp/static/images/'+stock+'.png')
      print('predict_stock 그래프 저장 완료')
      
      # 이동평균선 보고 배열도 분석
      if stock_df['5'].iloc[-1]>stock_df['60'].iloc[-1] and stock_df['20'].iloc[-1]>stock_df['60'].iloc[-1] and stock_df['60'].iloc[-1]>stock_df['120'].iloc[-1]:
          recom = '정배열(상승 추세)'
      elif stock_df['5'].iloc[-1]<stock_df['60'].iloc[-1] and stock_df['20'].iloc[-1]<stock_df['60'].iloc[-1] and stock_df['60'].iloc[-1]<stock_df['120'].iloc[-1]:
          recom = '역배열(하강 추세)'
      else:
          recom = '현재 배열 상태 없음'

      # 이동평균선 보고 크로스 분석   
      if stock_df['5'].iloc[-20]<stock_df['20'].iloc[-20] and stock_df['5'].iloc[-1]>stock_df['20'].iloc[-1]:
          cross = '단기 골든 크로스(상승 추세)'
      elif stock_df['5'].iloc[-20]>stock_df['20'].iloc[-20] and stock_df['5'].iloc[-1]<stock_df['20'].iloc[-1]:
          cross = '단기 데드 크로스(하강 추세)'

      elif stock_df['20'].iloc[-20]<stock_df['60'].iloc[-20] and stock_df['20'].iloc[-1]>stock_df['60'].iloc[-1]:
          cross = '중기 골든 크로스(상승 추세)'
      elif stock_df['20'].iloc[-20]>stock_df['60'].iloc[-20] and stock_df['20'].iloc[-1]<stock_df['60'].iloc[-1]:
          cross = '중기 데드 크로스(하강 추세)'
        
      elif stock_df['60'].iloc[-20]<stock_df['120'].iloc[-20] and stock_df['60'].iloc[-1]>stock_df['120'].iloc[-1]:
          cross = '장기 골든 크로스(상승 추세)'
      elif stock_df['60'].iloc[-20]>stock_df['120'].iloc[-20] and stock_df['60'].iloc[-1]<stock_df['120'].iloc[-1]:
          cross = '장기 데드 크로스(하강 추세)'
      
      elif stock_df['5'].iloc[-40]<stock_df['60'].iloc[-40] and stock_df['5'].iloc[-1]>stock_df['60'].iloc[-1] and stock_df['20'].iloc[-40]<stock_df['60'].iloc[-40] and stock_df['20'].iloc[-1]>stock_df['60'].iloc[-1] and stock_df['5'].iloc[-20]<stock_df['120'].iloc[-20] and stock_df['5'].iloc[-1]>stock_df['120'].iloc[-1] and stock_df['20'].iloc[-20]<stock_df['120'].iloc[-20] and stock_df['20'].iloc[-1]>stock_df['120'].iloc[-1]:
          cross = '강항 상승 추세'
      else:
          cross = '현재 크로스 상태 없음'


      # SVM으로 다음날 주식 가격 예측
      stock_df_td = stock_df.tail(200) # 최근200일정도만 training

      # stock_df_train = stock_df.tail(len(stock_df_td)-1) # 확인용 (개발자 외 사용금지)
      stock_df_close = stock_df_td['Close']
      stock_df_close = stock_df_close.values

      days=[]
      for i in range(1,len(stock_df_td)+1):
          days.append([int(i)])

      # training
      rbf_svr = SVR(kernel='rbf', C=100000, gamma=0.00001)
      rbf_svr.fit(days,stock_df_close)
      print('rbf 완료')
      # lin_svr = SVR(kernel="linear", C=10000)
      # lin_svr.fit(days,stock_df_close)
      # print('lin 완료')
      # poly_svr = SVR(kernel="poly", C=10000, degree=2)
      # poly_svr.fit(days,stock_df_close)
      # print('poly 완료')
      # predict
      day = [[len(days)+1]]
      rbf = rbf_svr.predict(day) # 성능 가장 좋음
      rbf = round(rbf[0],2)
      # print("Linear SVR 예측가격:",lin_svr.predict(day))
      # print("Poly SVR 예측가격:",poly_svr.predict(day))

      print(stock, ": ",recom, rbf, cross)
    return recom, rbf, cross
    

# %%
