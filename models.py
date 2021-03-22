# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler,RobustScaler,StandardScaler,Normalizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn import svm
from sklearn import metrics
import matplotlib.pyplot as plt
# from mlxtend.plotting import plot_decision_regions

cheat_data = pd.read_csv('cheat_svm.csv') 
ncheat_data = pd.read_csv('non_cheat_svm.csv')
del cheat_data['Unnamed: 0']

del ncheat_data['Unnamed: 0']
cheat_data[['Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = MinMaxScaler().fit_transform(cheat_data[['Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
ncheat_data[['Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = MinMaxScaler().fit_transform(ncheat_data[['Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
# cheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = Normalizer().fit_transform(cheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
# ncheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = Normalizer().fit_transform(ncheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
cheat_data = cheat_data.assign(result=[1]*cheat_data.shape[0])
ncheat_data = ncheat_data.assign(result=[0]*ncheat_data.shape[0])
cheat_data = cheat_data.assign(result=[1]*cheat_data.shape[0])
ncheat_data = ncheat_data.assign(result=[0]*ncheat_data.shape[0])

df = pd.concat([cheat_data,ncheat_data])

df = df.sample(frac=1).reset_index(drop=True) 

X = df.iloc[:,:-1]
y = df.iloc[:,-1]

print((X.iloc[1]).shape)
X_train, X_test, y_train, y_test = train_test_split(X, y,stratify=y, test_size=0.25)
# model = LinearRegression().fit(X_train,y_train)
model = svm.SVC(kernel='poly',gamma="scale",probability=True)
model.fit(X_train,y_train)
# y_pred = model.predict(X_test)

# v = X_train.mean()
# filler_values = {}
# for i in range(6):
#     filler_values[i] = v[i]

# plot_decision_regions(X=np.array(X_train[:100]), 
#                       y=np.array(y_train[:100]),
#                       clf=model, 
#                       filler_feature_values=filler_values,
#                       legend=2)

# plt.xlabel(X_train.columns[0], size=14)
# plt.ylabel(X_train.columns[1], size=14)
# plt.title('SVM Decision Region Boundary', size=16)
# plt.show()
# score = metrics.accuracy_score(y_test, y_pred)

# logistic_model = LogisticRegression()
# logistic_model.fit(X_train,y_train)
# model = logistic_model
# y_pred = logistic_model.predict(X_test)
# score = logistic_model.score(X_test,y_test)
# print(score)

# z=pd.Series([1.0, 0.5393258426966292,0.9448818897637795,0.0,0.0,0.5818178686259597])
# print(z.shape)
# print(model.predict(X.iloc[1]))

def final_predictor(arr):
    cheating=model.predict_proba(arr)
    # cheating = model.predict(arr)
    # if(cheating[0][0] > 0.7):
    #     print('cheat detected')
    return cheating

