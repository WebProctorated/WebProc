# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn import metrics

path = './proctoring/dataset/'
cheat_data1 = pd.read_csv(path+'class1.csv')
cheat_data2 = pd.read_csv(path+'class2.csv')
cheat_data3 = pd.read_csv(path+'class3.csv')
cheat_data4 = pd.read_csv(path+'class4.csv')
cheat_data5 = pd.read_csv(path+'class5.csv')
cheat_data6 = pd.read_csv(path+'class6.csv')
cheat_data7 = pd.read_csv(path+'class7.csv')
ncheat_data = pd.read_csv(path+'class0.csv')
del cheat_data1['Unnamed: 0']
del cheat_data2['Unnamed: 0']
del cheat_data3['Unnamed: 0']
del cheat_data4['Unnamed: 0']
del cheat_data5['Unnamed: 0']
del cheat_data6['Unnamed: 0']
del cheat_data7['Unnamed: 0']
del ncheat_data['Unnamed: 0']
cheat_data1[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(cheat_data1[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])
cheat_data2[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(cheat_data2[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])
cheat_data3[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(cheat_data3[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])
cheat_data4[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(cheat_data4[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])
cheat_data5[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(cheat_data5[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])
cheat_data6[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(cheat_data6[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])
cheat_data7[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(cheat_data7[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])

ncheat_data[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']] = MinMaxScaler(
).fit_transform(ncheat_data[['Angle1', 'Angle2', 'cnt_inner', 'cnt_outer', 'Phone_detected']])
cheat_data1 = cheat_data1.assign(result=[1]*cheat_data1.shape[0])
cheat_data2 = cheat_data2.assign(result=[1]*cheat_data2.shape[0])
cheat_data3 = cheat_data3.assign(result=[1]*cheat_data3.shape[0])
cheat_data4 = cheat_data4.assign(result=[1]*cheat_data4.shape[0])
cheat_data5 = cheat_data5.assign(result=[1]*cheat_data5.shape[0])
cheat_data6 = cheat_data6.assign(result=[1]*cheat_data6.shape[0])
cheat_data7 = cheat_data7.assign(result=[1]*cheat_data7.shape[0])
ncheat_data = ncheat_data.assign(result=[0]*ncheat_data.shape[0])


df = pd.concat([cheat_data1, cheat_data2, cheat_data3, cheat_data4,
                cheat_data5, cheat_data6, cheat_data7, ncheat_data])

df = df.sample(frac=1).reset_index(drop=True)

X = df.iloc[:, :-1]
y = df.iloc[:, -1]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
model = LinearRegression()
model.fit(X_train, y_train)
#model = SVM(kernel='sigmoid',gamma='scale')
# model.fit(X_train,y_train)
y_pred = model.predict(X_train)
#score = metrics.accuracy_score(y_test, y_pred)
#print("Accuracy is", score)
#cm = metrics.confusion_matrix(y_test, y_pred)
# print(cm)


def final_predictor(arr):
    cheating = model.predict(arr)
    return cheating
