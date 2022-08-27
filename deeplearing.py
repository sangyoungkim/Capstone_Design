#딥러닝 공부 
#데이터 베이스 링크  =  https://github.com/blackdew/tensorflow1/master/csv/lemonade.csv


#1. 라이브러리 사용
import tensorflow as tf
import pandas as pd

#2.데이터 준비
파일경로 = 'https://raw.githubusercontent.com/blackdew/tensorflow1/master/csv/lemonade.csv'
레모네이드 = pd.read_csv(파일경로)
독립 = 레모네이드[['온도']]
종속 = 레모네이드[['판매량']]
#print(독립.shape, 종속.shape) #데이터 분리 정확도 확인

#.모델을 만든다.
x = tf.keras.layers.Input(shape = [1]) 
# 1은 독립변수의 칼럼의 갯수가 하나이기 때문
y = tf.keras.layers.Dense(1)(x)
model = tf.keras.models.Model(x,y)
model.compile(loss = 'mse')

#4. 모델을 학습한다.
model.fit(독립,종속,epochs=1000,verbose = 0)
model.fit(독립,종속,epochs=10)
print(model.predict([20,21]))
#verbose 는 학습상황 출력안시킴