# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler,RobustScaler,StandardScaler,Normalizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn import svm
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
# from mlxtend.plotting import plot_decision_regions

# cheat_data = pd.concat([pd.read_csv('cheat_svm.csv'),pd.read_csv('cheating.csv')]) 
# ncheat_data = pd.concat([pd.read_csv('non_cheat_svm.csv'),pd.read_csv('non_cheating.csv')])
class0 = pd.read_csv('class0.csv')
class0 = class0.assign(result=[0]*class0.shape[0])
class1 = pd.read_csv('class1.csv')
class1 = class1.assign(result=[1]*class1.shape[0])
class2 = pd.read_csv('class2.csv')
class2 = class2.assign(result=[2]*class2.shape[0])
class3 = pd.read_csv('class3.csv')
class3 = class3.assign(result=[3]*class3.shape[0])
class4 = pd.read_csv('class4.csv')
class4 = class4.assign(result=[4]*class4.shape[0])
class5 = pd.read_csv('class5.csv')
class5 = class5.assign(result=[5]*class5.shape[0])
class6 = pd.read_csv('class6.csv')
class6 = class6.assign(result=[6]*class6.shape[0])
class7 = pd.read_csv('class7.csv')
class7 = class7.assign(result=[7]*class7.shape[0])
# class1 = pd.read_csv('class0.csv')
# class1 = class0.assign(result=[0]*class0.shape[0])
# cheat_data = class0
# ncheat_data = pd.concat([class1,class2,class3,class4,class5,class6,class7])
# cheat_data = pd.read_csv('cheat_dummy_data.csv')
# ncheat_data = pd.read_csv('non_cheating.csv')
df = pd.concat([class0,class1,class2,class3,class4,class5,class6,class7])
del df['Unnamed: 0']

# del ncheat_data['Unnamed: 0']
df[['Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = MinMaxScaler().fit_transform(df[['Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
# ncheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = MinMaxScaler().fit_transform(ncheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
# cheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = Normalizer().fit_transform(cheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
# ncheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']] = Normalizer().fit_transform(ncheat_data[['no_faces','Angle1','Angle2','cnt_inner','cnt_outer','Phone_detected']])
# cheat_data = cheat_data.assign(result=[1]*cheat_data.shape[0])
# ncheat_data = ncheat_data.assign(result=[0]*ncheat_data.shape[0])
# cheat_data = cheat_data.assign(result=[1]*cheat_data.shape[0])
# ncheat_data = ncheat_data.assign(result=[0]*ncheat_data.shape[0])

# df = pd.concat([cheat_data,ncheat_data])

df = df.sample(frac=1).reset_index(drop=True) 

X = df.iloc[:,:-1]
y = df.iloc[:,-1]

print((X.iloc[1]).shape)
X_train, X_test, y_train, y_test = train_test_split(X, y,stratify=y, test_size=0.25)
# model = LinearRegression().fit(X_train,y_train)
model = svm.SVC(gamma='scale',probability=True)
model.fit(X_train,y_train)
# model = DecisionTreeClassifier(random_state=10)
# model.fit(X_train,y_train)
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

