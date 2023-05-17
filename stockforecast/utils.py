import csv
from datetime import datetime, date, timedelta
from .models import *
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from dateutil.relativedelta import relativedelta


def save_stock_data_from_csv(filepath, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    full_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'historicaldata', filepath)
    with open(full_filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # Move the next() call inside the with block
        next(reader) # skip the header row

        # loop through each row in the CSV file and save as a model object
        for row in reader:
            date = None
            if row[0].count('/') == 2: # check if the date format is mm/dd/yyyy
                date = datetime.strptime(row[0], '%m/%d/%Y').date()
            elif row[0].count('-') == 2: # check if the date format is yyyy-mm-dd
                date = datetime.strptime(row[0], '%Y-%m-%d').date()
            else: # set date to None if the format is not recognized
                print(f"Invalid date format in CSV file for symbol {symbol}: {row[0]}")
                continue
            # date = datetime.strptime(row[0], '%m/%d/%Y').date()
            open_price = float(row[1]) if row[1] != "null" else 0.0
            high_price = float(row[2]) if row[2] != "null" else 0.0
            low_price = float(row[3]) if row[3] != "null" else 0.0
            close_price = float(row[4]) if row[4] != "null" else 0.0
            adj_close = float(row[5]) if row[5] != "null" else 0.0
            volume = int(row[6]) if row[6] != "null" else 0

            # create a new StockPrice object and save to the database
            stock_price = StockPrice(stock=stock, date=date, open_price=open_price, high_price=high_price, low_price=low_price,
                                 close_price=close_price, adj_close_price=adj_close, volume=volume)

            stock_price.save()

# def save_lstm_predict(symbol):

    # First, get the stock object that you want to add forecasted values for
    stock = Stock.objects.get(name=symbol)

    # Then, open the CSV file and read the data
    with open('stockforecast/lstmforecasts/AASIA_lstm.csv', 'r') as f:
    # full_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lstmforecasts', filepath)
    # with open(full_filepath, 'r') as csvfile:
        reader = csv.reader(f)
        next(reader)  # skip the header row
    for row in reader:
        period = row[0]
        year_or_day = row[1]
        value = float(row[2])
        
        # Create a date object based on the period and year/day
        if period == 'Days':
            forecast_date = date.today() + timedelta(days=int(year_or_day))
        elif period == 'Weeks':
            forecast_date = date.today() + timedelta(weeks=int(year_or_day))
        elif period == 'Months':
            forecast_date = date.today() + relativedelta(months=int(year_or_day))
        elif period == 'Years':
            forecast_date = date(int(year_or_day), 12, 31)
        
        # Create a new instance of LstmForecastedValue
        forecast = LstmForecastedValue()
        
        # Set the foreign key and date fields
        forecast.stock = stock
        forecast.date = forecast_date
        
        # Set the values for the arrays
        if period == 'Days':
            forecast.next_five_days_values = [value] * 5
        elif period == 'Weeks':
            forecast.next_five_weeks_values = [value] * 5
        elif period == 'Months':
            forecast.next_five_months_values = [value] * 5
        elif period == 'Years':
            forecast.next_five_years_values = [value] * 5
        
        # Finally, save the instance to the database
        forecast.save()
        
def save_lstm_predict(symbol):
    # First, get the stock object that you want to add forecasted values for
    stock = Stock.objects.get(symbol=symbol)

    # Construct the file path based on the symbol parameter
    file_path = os.path.join("stockforecast", "lstmforecasts", f"{symbol}_lstm.csv")

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row

        # Default values for all next_X_day variables
        next_1_day = 0
        next_2_day = 0
        next_3_day = 0
        next_4_day = 0
        next_5_day = 0

        # Default values for all next_X_week variables
        next_1_week = 0
        next_2_week = 0
        next_3_week = 0
        next_4_week = 0
        next_5_week = 0

        # Default values for all next_X_month variables
        next_1_month = 0
        next_2_month = 0
        next_3_month = 0
        next_4_month = 0
        next_5_month = 0

        # Default values for all next_X_year variables
        next_1_year = 0
        next_2_year = 0
        next_3_year = 0
        next_4_year = 0
        next_5_year = 0

        for row in reader:
            period, num_periods, value = row
            value = float(value)

            # Set the correct forecasted value based on the period and num_periods
            if period == 'Days':
                if num_periods == '1':
                    next_1_day = value
                elif num_periods == '2':
                    next_2_day = value
                elif num_periods == '3':
                    next_3_day = value
                elif num_periods == '4':
                    next_4_day = value
                elif num_periods == '5':
                    next_5_day = value
            elif period == 'Weeks':
                if num_periods == '1':
                    next_1_week = value
                elif num_periods == '2':
                    next_2_week = value
                elif num_periods == '3':
                    next_3_week = value
                elif num_periods == '4':
                    next_4_week = value
                elif num_periods == '5':
                    next_5_week = value
            elif period == 'Months':
                if num_periods == '1':
                    next_1_month = value
                elif num_periods == '2':
                    next_2_month = value
                elif num_periods == '3':
                    next_3_month = value
                elif num_periods == '4':
                    next_4_month = value
                elif num_periods == '5':
                    next_5_month = value
            elif period == 'Years':
                if num_periods == '2023':
                    next_1_year = value
                elif num_periods == '2024':
                    next_2_year = value
                elif num_periods == '2025':
                    next_3_year = value
                elif num_periods == '2026':
                    next_4_year = value
                elif num_periods == '2027':
                    next_5_year = value


    # Create a new LstmForecastedValue object with the forecasted values
    lstm_forecast = LstmForecastedValue(
        stock=stock,
        date="2023-04-23",
        next_1_day = next_1_day,
        next_2_day = next_2_day,
        next_3_day = next_3_day,
        next_4_day = next_4_day,
        next_5_day = next_5_day,
        next_1_week = next_1_week,
        next_2_week = next_2_week,
        next_3_week = next_3_week,
        next_4_week = next_4_week,
        next_5_week = next_5_week,
        next_1_month = next_1_month,
        next_2_month = next_2_month,
        next_3_month = next_3_month,
        next_4_month = next_4_month,
        next_5_month = next_5_month,
        next_1_year = next_1_year,
        next_2_year = next_2_year,
        next_3_year = next_3_year,
        next_4_year = next_4_year,
        next_5_year = next_5_year,
    )

    # Save the object to the database
    lstm_forecast.save()

    print(lstm_forecast)

def save_mlp_predict(symbol):
    # First, get the stock object that you want to add forecasted values for
    stock = Stock.objects.get(symbol=symbol)

    # Construct the file path based on the symbol parameter
    file_path = os.path.join("stockforecast", "mlpforecasts", f"{symbol}_mlp.csv")

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row

        # Default values for all next_X_day variables
        next_1_day = 0
        next_2_day = 0
        next_3_day = 0
        next_4_day = 0
        next_5_day = 0

        # Default values for all next_X_week variables
        next_1_week = 0
        next_2_week = 0
        next_3_week = 0
        next_4_week = 0
        next_5_week = 0

        # Default values for all next_X_month variables
        next_1_month = 0
        next_2_month = 0
        next_3_month = 0
        next_4_month = 0
        next_5_month = 0

        # Default values for all next_X_year variables
        next_1_year = 0
        next_2_year = 0
        next_3_year = 0
        next_4_year = 0
        next_5_year = 0

        for row in reader:
            period, num_periods, value = row
            value = float(value)

            # Set the correct forecasted value based on the period and num_periods
            if period == 'Days':
                if num_periods == '1':
                    next_1_day = value
                elif num_periods == '2':
                    next_2_day = value
                elif num_periods == '3':
                    next_3_day = value
                elif num_periods == '4':
                    next_4_day = value
                elif num_periods == '5':
                    next_5_day = value
            elif period == 'Weeks':
                if num_periods == '1':
                    next_1_week = value
                elif num_periods == '2':
                    next_2_week = value
                elif num_periods == '3':
                    next_3_week = value
                elif num_periods == '4':
                    next_4_week = value
                elif num_periods == '5':
                    next_5_week = value
            elif period == 'Months':
                if num_periods == '1':
                    next_1_month = value
                elif num_periods == '2':
                    next_2_month = value
                elif num_periods == '3':
                    next_3_month = value
                elif num_periods == '4':
                    next_4_month = value
                elif num_periods == '5':
                    next_5_month = value
            elif period == 'Years':
                if num_periods == '2023':
                    next_1_year = value
                elif num_periods == '2024':
                    next_2_year = value
                elif num_periods == '2025':
                    next_3_year = value
                elif num_periods == '2026':
                    next_4_year = value
                elif num_periods == '2027':
                    next_5_year = value


    # Create a new MlpForecastedValue object with the forecasted values
    mlp_forecast = MLPForecastedValue(
        stock=stock,
        date="2023-04-23",
        next_1_day = next_1_day,
        next_2_day = next_2_day,
        next_3_day = next_3_day,
        next_4_day = next_4_day,
        next_5_day = next_5_day,
        next_1_week = next_1_week,
        next_2_week = next_2_week,
        next_3_week = next_3_week,
        next_4_week = next_4_week,
        next_5_week = next_5_week,
        next_1_month = next_1_month,
        next_2_month = next_2_month,
        next_3_month = next_3_month,
        next_4_month = next_4_month,
        next_5_month = next_5_month,
        next_1_year = next_1_year,
        next_2_year = next_2_year,
        next_3_year = next_3_year,
        next_4_year = next_4_year,
        next_5_year = next_5_year,
    )

    # Save the object to the database
    mlp_forecast.save()

    print(mlp_forecast)

