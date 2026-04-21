# Scrum Team 6 | INFOTC-4320-Stock-Data-Visualizer
# Importing flask and adding functionality:
from flask import Flask, render_template

app = flask(__name__)
app.config['KEY'] = 'API_KEY'

# ======= STOCK SYMBOL (Mia) =======
def get_stock_symbol():
    #Ask user for stock symbol and validate input
    #returns a valid, uppercase stock symbol

    while True:
        symbol = input("Enter the stock symbol you are looking for: ").strip().upper()
        if len(symbol) == 0:
            print("Invalid input! Please try again.\n")
        elif not symbol.isalpha():
            print("Invalid input! Stock symbols should only contain letters. Please try again.\n")
        else:
            return symbol
        

# ======= SELECT CHART (Trent) =======
def SelectChart():
    while True:
        try:    
            # Ask user for input and validate their choice
            ChartInput = int(input("Please select a chart type:\n 1. Line Graph\n 2. Bar Graph\n\n Selection: "))
            if ChartInput == 1 or ChartInput ==2:
                return ChartInput
            elif ChartInput != 1 or ChartInput != 2:
                print("Invalid integer, please try again.") 
            else:
                return SelectChart()
        # Making sure that a person's input is not a string
        except ValueError:
            print("Input must be the integer 1 or 2")

# ======= TIME SERIES (Ben) =======
def time_series_menu():
    
    while True:
    
        print("Select the Time Series of the chart you want to Generate\n----------------------------------------------")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly")

        time_series = input("Enter the time series option (1, 2, 3, 4): ")
        if time_series == "1":
            return 1
        elif time_series == "2":
            return 2
        elif time_series == "3":
            return 3
        elif time_series == "4":
            return 4
        else: 
            print("ERROR: input is invalid try again...")
            continue

def get_time_series_label(time_series_type):
    if time_series_type == 1:
        return "Intraday"
    elif time_series_type == 2:
        return "Daily"
    elif time_series_type == 3:
        return "Weekly"
    elif time_series_type == 4:
        return "Monthly"
    
# ======= TIME SERIES QUERY (Mia) =======
def querying_api(time_series_type, stock_symbol, API_KEY):
    try:
        import requests
    except:
        print("\nFailed to import requests")

    while True:
        if time_series_type == 1:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={API_KEY}'
            r = requests.get(url)
            data = r.json()
            return data
        elif time_series_type == 2:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={API_KEY}'
            r = requests.get(url)
            data = r.json()
            return data
        elif time_series_type == 3:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock_symbol}&apikey={API_KEY}'
            r = requests.get(url)
            data = r.json()
            return data
        elif time_series_type == 4:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock_symbol}&apikey={API_KEY}'
            r = requests.get(url)
            data = r.json()
            return data
        else:
            print("Error!")

# ======= YYYY-MM-DD [Begin & End] (Sebastian) =======
def get_begin_date():

    while True:

        # Gather Input
        begin_date = input("\nPlease enter beginning date (YYYY-MM-DD): ")

        # Validate 
        if is_date_valid(begin_date):
            return begin_date

def get_end_date():
        
        while True:

            # Gather Input
            end_date = input("\nPlease enter ending date (YYYY-MM-DD): ")

            # Validate 
            if is_date_valid(end_date):
                return end_date

def is_date_valid(selected_date):

    # Make sure string isn't empty
    if len(selected_date) == 0:
            print("\nERROR: Beginning Date should not be null")

    # Strip and convert to date-time format
    try:
        import datetime

        datetime.datetime.strptime(selected_date, "%Y-%m-%d")
        return True
    except:
        print("\nERROR: Input is not in correct YYYY-MM-DD format")
        return False
    
def validate_dates(begin_date, end_date):
    try:
        import datetime

        # Restrip and convert to date-time format
        begin = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # If beginning date is less than end date
        if begin < end:
            return True
        else:
            print("\nERROR: Dates are not correctly selected")
            return False

    # Date parsing failed
    except:
        print("\nERROR: Invalid date format")
        return False

# GRAPH GENERATION (Trent)

def GraphGeneration(data, ChartInput, start_date, end_date, symbol, time_series_type):
    import pygal
    import csv
    
    # Set the keys to the input according to their json values:
    if time_series_type == 1:
        TimeKey = "Time Series (5min)"
    elif time_series_type == 2:
        TimeKey = "Time Series (Daily)"
    elif time_series_type == 3:
        TimeKey = "Weekly Time Series"
    elif time_series_type == 4:
        TimeKey = "Monthly Time Series"
    else:
        print("Value Error, please try again")
        return
    
    # Get the stock data from the four different points and put it into a dictionary
    # Uses the key value pair "1. open : 323.45", for example
    StockData = data.get(TimeKey, {})

    # Check that the API actually returned data
    if not StockData:
        print(f"No data found. API response keys were: {list(data.keys())}")
        return
    
    # Get the dates
    GraphDates = []
    for date in StockData:
        date_only = date[:10]  # Handles both "YYYY-MM-DD" and "YYYY-MM-DD HH:MM:SS"
        if date_only >= start_date and date_only <= end_date:
            GraphDates.append(date)
            
    # Sort the dates from least to most recent
    GraphDates.sort()

    # Check that dates entered fall within the available data range
    if not GraphDates:
        print(f"No data found between {start_date} and {end_date}.")
        print(f"Available date range: {min(StockData)[:10]} to {max(StockData)[:10]}")
        return
    
    # Creating separate lists for the four types we need to graph
    High = []
    Low = []
    Open = []
    Close = []
        
    # Assigning the values from the json values to the list
    for date in GraphDates:
        Open.append(float(StockData[date]["1. open"]))
        High.append(float(StockData[date]["2. high"]))
        Low.append(float(StockData[date]["3. low"]))
        Close.append(float(StockData[date]["4. close"]))
        
    # CHART SETUP
    
    # Create the chart
    try:
        if ChartInput == 1:
            chart = pygal.Line()
        else:
            chart = pygal.Bar()
    except:
        print("Value Error")
        return
    
    # Set the chart title and labels
    chart.title = f"Stock Data for {symbol}: {start_date} to {end_date}"
    
    chart.x_labels = GraphDates
    chart.add('Open', Open)
    chart.add('Close', Close)
    chart.add('High', High)
    chart.add('Low', Low)

    chart.render_to_file(f"{symbol}_chart.svg")
    print(f"Chart saved as {symbol}_chart.svg")

# ============== MAIN FUNCTION ==============
def main():

    # == API KEY ==:
    API_KEY = "T5LLNYG4DQCQB5QI"

    # == Stock Symbol ==
    stock_symbol = get_stock_symbol()

    # == Chart Select ==
    ChartInput = SelectChart()

    # == Time Series ==
    time_series_type = time_series_menu()
    
    # == Date Selection ==
    begin_date = get_begin_date()
    end_date = get_end_date()

    if not validate_dates(begin_date, end_date):
        print("Please restart and enter a valid date range.")
        return

    data = querying_api(time_series_type, stock_symbol, API_KEY)
    GraphGeneration(data, ChartInput, begin_date, end_date, stock_symbol, time_series_type)
    
main()