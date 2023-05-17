import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense, LSTM
from .models import *
from django.db.models import Q
import datetime
import matplotlib.pyplot as plt
from django.shortcuts import get_object_or_404
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def make_predictions_years():

    # Set file path
    filename = 'AASIA.csv'
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'historicaldata', filename)

    # Load data using csv.reader
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) # read header row
        data = []
        for row in reader:
            data.append(row)
        df = pd.DataFrame(data, columns=header)
    

    # Convert date column to datetime object and set it as index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Select only the 'Close' column and split data into training and testing sets
    train_data = df[['Close']].iloc[:-2487]
    test_data = df[['Close']].iloc[-2487:]

    # Convert all the values in train_data to numeric after replacing 'null' with NaN
    train_data = train_data.replace('null', np.nan).fillna(0).apply(pd.to_numeric)
    test_data = test_data.replace('null', np.nan).fillna(0).apply(pd.to_numeric)

    # Normalize data
    scaler = MinMaxScaler()
    train_data = scaler.fit_transform(train_data.values)
    test_data = scaler.transform(test_data.values)

    # Replace 'null' values with 0
    train_data = pd.DataFrame(train_data).replace('null', 0).values
    test_data = pd.DataFrame(test_data).replace('null', 0).values

    # Create input sequences and corresponding output values
    def create_sequences(data, seq_length):
        X = []
        y = []
        for i in range(seq_length, len(data)):
            X.append(data[i-seq_length:i])
            y.append(data[i]) # Assuming that the target variable is the 'Open' column
        return np.array(X), np.array(y)

    seq_length = 365
    X_train, y_train = create_sequences(train_data, seq_length)
    X_test, y_test = create_sequences(test_data, seq_length)

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(128, input_shape=(seq_length, train_data.shape[1])))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # Train model
    model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test))

    # Use the model to make predictions on the test set
    y_pred = model.predict(X_test)

    # Inverse transform the scaled values to the original scale
    y_pred = scaler.inverse_transform(y_pred)
    y_test = scaler.inverse_transform(y_test)

    # Plot the actual vs predicted values
    # plt.plot(y_test, label='Actual')
    # plt.plot(y_pred, label='Predicted')
    # plt.legend()
    # plt.xlim([0, len(y_test)])
    # plt.show()

    # Define the prediction periods
    periods = {
        'days': 5,
        'weeks': 5*7,
        'months': 5*30,
        'years': 5*365
    }

    # Make predictions for each period and save to CSV file
    with open('AASIA_predicted_close_prices.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Period', 'Year', 'Close Price'])
        
        # Predict for the next 5 days
        last_seq = test_data[-seq_length:]
        forecast_day = []
        for i in range(periods['days']):
            pred = model.predict(last_seq.reshape(1, seq_length, 1))
            forecast_day.append(pred[0][0])
            last_seq = np.append(last_seq[1:], pred[0]).reshape(seq_length, 1)
        forecast_day = scaler.inverse_transform(np.array(forecast_day).reshape(-1, 1))
        for i in range(5):
            close_price = forecast_day[i][0]
            writer.writerow(['Days', i+1, close_price])
            print(f"Day {i+1}: {close_price:.6f}")
            print("\n")

        # Predict for the next 5 weeks
        forecast_week = []
        for i in range(periods['weeks']):
            pred = model.predict(last_seq.reshape(1, seq_length, 1))
            forecast_week.append(pred[0][0])
            last_seq = np.append(last_seq[1:], pred[0]).reshape(seq_length, 1)
        forecast_week = scaler.inverse_transform(np.array(forecast_week).reshape(-1, 1))
        for i in range(5):
            close_price = forecast_week[i][0]
            writer.writerow(['Weeks', i+1, close_price])
            print(f"Week {i+1}: {close_price:.6f}")
            print("\n")
        
        # Predict for the next 5 months
        forecast_month = []
        for i in range(periods['months']):
            pred = model.predict(last_seq.reshape(1, seq_length, 1))
            forecast_month.append(pred[0][0])
            last_seq = np.append(last_seq[1:], pred[0]).reshape(seq_length, 1)
        forecast_month = scaler.inverse_transform(np.array(forecast_month).reshape(-1, 1))
        for i in range(5):
            close_price = forecast_month[i][0]
            writer.writerow(['Months', i+1, close_price])
            print(f"Month {i+1}: {close_price:.6f}")
            print("\n")

        # Predict for the next 5 years
        forecast_year = []
        for i in range(periods['years']):
            pred = model.predict(last_seq.reshape(1, seq_length, 1))
            forecast_year.append(pred[0][0])
            last_seq = np.append(last_seq[1:], pred[0]).reshape(seq_length, 1)
        forecast_year = scaler.inverse_transform(np.array(forecast_year).reshape(-1, 1))
        for i in range(2023, 2028):
            close_price = forecast_year[i-2023][0]
            writer.writerow(['Years',i, close_price])
            print(f"4/23/{i}: {forecast_year[i-2023][0]:.6f}")
            print("\n")

