import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas_datareader.data as data
from keras.models import load_model
from tensorflow.keras.models import load_model
import streamlit as st

import yfinance as yf

# Define the start and end dates
start = '2010-01-01'
end = '2019-12-31'

st.title('Stock Trend Prediction')


user_input= st.text_input('Enter Stock Ticker', 'AAPL')
# Fetch the data 
df = yf.download(user_input, start=start, end=end)

#describing data
st.subheader('Data from 2010 - 2019')
st.write(df.describe())

#VISUALIZTIONS

st.subheader('Closing Price vs Time Chart with 100MA')
ma100=df.Close.rolling(100).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
ma100=df.Close.rolling(100).mean()
ma200=df.Close.rolling(200).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)

#splitting data into training and testing

data_training=pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing= pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler(feature_range=(0,1))

data_training_array=scaler.fit_transform(data_training)


#LOAD MY MODEL

model=load_model('keras_model.h5')

#testing part

past_100_days=data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)

input_data=scaler.fit_transform(final_df)

x_test=[]
y_test=[]

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i,0])
    
x_test, y_test = np.array(x_test), np.array(y_test)
print(x_test.shape)
print(y_test.shape)

y_predicted=model.predict(x_test)
scaler= scaler.scale_

scale_factor=1.0/scaler[0]
y_predicted=y_predicted*scale_factor
y_test=y_test*scale_factor


#final graph

st.subheader('Predictions vs Orignal')

fig2=plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label='Orignal Price')
plt.plot(y_predicted, 'r', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

