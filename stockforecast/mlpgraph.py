import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.optimizers import Adam
from .models import *
import os
import csv



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

    # Build MLP model
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(seq_length,)))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer=Adam(lr=0.001), loss='mse')

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=2)

    # Evaluate the model on the test set
    loss = model.evaluate(X_test, y_test, verbose=0)
    print(f'Test set loss: {loss:.4f}')

    # Use the model to make predictions on the test set
    predictions = model.predict(X_test)

    # Inverse transform the predicted and actual values to their original scale
    predictions = scaler.inverse_transform(predictions)
    actuals = scaler.inverse_transform(y_test)

    # Print the actual and predicted values for the last 5 days in the test set
    last_5_days = -5
    print('Actual and predicted stock prices for the last 5 days in the test set:')
    for i in range(last_5_days, 0):
        print(f'Actual: {actuals[i][0]:.6f}, Predicted: {predictions[i][0]:.6f}')
    
    with open('mlp_prices.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Period', 'Interval', 'Close Price'])

# days
        last_sequence = X_test[-1:]
        next_years = []
        for i in range(5):
            next_day = model.predict(last_sequence)[0]
            next_years.append(next_day[0])
            last_sequence = np.append(last_sequence[:,1:,:], [[next_day]], axis=1)

        # Convert the predicted values to their original scale
        next_years = np.array(next_years).reshape(-1, 1)
        next_years = scaler.inverse_transform(next_years)

        # Print the predicted values for the next 5 days
        print('Predicted for next 5 days:')
        for i in range(5):
            pred_price = next_years[i][0]
            writer.writerow(['Days', i+1, pred_price])
            print(f'{pred_price:.6f}')
        
# weeks
        last_sequence = X_test[-1:]
        next_five_weeks = []
        for i in range(5*7):
            next_day = model.predict(last_sequence)[0]
            next_five_weeks.append(next_day[0])
            last_sequence = np.append(last_sequence[:,1:,:], [[next_day]], axis=1)

        # Convert the predicted values to their original scale
        next_five_weeks = np.array(next_five_weeks).reshape(-1, 1)
        next_five_weeks = scaler.inverse_transform(next_five_weeks)

        # Print the predicted values for the next 5 weeks
        print('Predicted for next 5 weeks:')
        for i in range(5):
            pred_price = next_five_weeks[(i+1)*7-1][0]
            writer.writerow(['Weeks', i+1, pred_price])
            print(f'{pred_price:.6f}')
        
# months
        last_sequence = X_test[-1:]
        next_months = []
        for i in range(5*30):
            next_day = model.predict(last_sequence)[0]
            next_months.append(next_day[0])
            last_sequence = np.append(last_sequence[:,1:,:], [[next_day]], axis=1)

        # Convert the predicted values to their original scale
        next_months = np.array(next_months).reshape(-1, 1)
        next_months = scaler.inverse_transform(next_months)

        # Print the predicted values for the next 5 months
        print('Predicted for next 5 months:')
        for i in range(5):
            pred_price = next_months[(i+1)*30-1][0]
            writer.writerow(['Months', i+1, pred_price])
            print(f'{pred_price:.6f}')
        
# years
        last_sequence = X_test[-1:]
        next_years = []
        for i in range(5*365):
            next_day = model.predict(last_sequence)[0]
            next_years.append(next_day[0])
            last_sequence = np.append(last_sequence[:,1:,:], [[next_day]], axis=1)

        # Convert the predicted values to their original scale
        next_years = np.array(next_years).reshape(-1, 1)
        next_years = scaler.inverse_transform(next_years)

        # Print the predicted values for the next 5 years
        print('Predicted for next 5 days:')
        for i in range(5):
            pred_price = next_years[(i+1)*365-1][0]
            writer.writerow(['Years', i+1, pred_price])
            print(f'{pred_price:.6f}')