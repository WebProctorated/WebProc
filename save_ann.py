import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib

class0 = pd.read_csv('class0.csv') # non cheat
class0 = class0.assign(result=[0]*class0.shape[0])
class1 = pd.read_csv('class1.csv') # head down
class1 = class1.assign(result=[1]*class1.shape[0])
class2 = pd.read_csv('class2.csv') # head left and talking
class2 = class2.assign(result=[2]*class2.shape[0])
class3 = pd.read_csv('class3.csv') # head right and talking
class3 = class3.assign(result=[3]*class3.shape[0])
class4 = pd.read_csv('class4.csv') # talking
class4 = class4.assign(result=[4]*class4.shape[0])
class5 = pd.read_csv('class5.csv') # phone+(head orientation change + talking)
class5 = class5.assign(result=[5]*class5.shape[0])
class6 = pd.read_csv('class6.csv') # No person in frame
class6 = class6.assign(result=[6]*class6.shape[0])
class7 = pd.read_csv('class7.csv') # more than 1 person in frame
class7 = class7.assign(result=[7]*class7.shape[0])


df = pd.concat([class0,class1,class2,class3,class4,class5,class6,class7])

del df['Unnamed: 0']

df = df.sample(frac=1).reset_index(drop=True) #shuffling

# train test split
# X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,:-1], df.iloc[:,-1], test_size=0.30)

# label split
X = df.iloc[:,:-1]
y = df.iloc[:,-1]

# scaling
scaler = MinMaxScaler()
X[X.columns] = scaler.fit_transform(X[X.columns])

# ANN
model = Sequential([
    Dense(units=12, input_dim=6, activation='relu'),
    Dense(units=24, activation='relu'),
    Dense(units=12,activation='relu'),
    Dense(units=24, activation='relu'),
    Dense(units=8, activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.01), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x=X.values, y=y.values, batch_size=10, epochs=100,shuffle=True, verbose=2)

# saving model
model.save('./cheat_predictor_model_v1.h5')

#saving scaler
joblib.dump(scaler, 'scaler_v1.gz')
