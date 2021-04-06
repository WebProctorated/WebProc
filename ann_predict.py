import tensorflow as tf
import joblib
import numpy as np

#loading model
saved_model = tf.keras.models.load_model('./cheat_predictor_model_v2.h5')

#loading scaler
saved_scaler = joblib.load('scaler_v2.gz')

def final_predictor(df):
    scaled_arr = saved_scaler.transform(df[df.columns])
    prediction = saved_model.predict(x=scaled_arr,verbose=0)
    rounded_prediction = np.argmax(prediction, axis=-1)
    return rounded_prediction