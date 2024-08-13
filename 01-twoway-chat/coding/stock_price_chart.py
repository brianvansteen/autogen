# filename: stock_price_chart.py

# Import necessary libraries
import requests
import matplotlib.pyplot as plt

# Alpha Vantage API key - Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'YOUR_API_KEY'

# Function to get stock price data from Alpha Vantage for a given symbol
def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url, timeout=10)  # Increase the timeout value to 10 seconds
    data = response.json()
    time_series = data['Time Series (Daily)']
    
    dates = []
    prices = []
    for date, values in time_series.items():
        dates.append(date)
        prices.append(float(values['4. close']))
    
    return dates, prices

# Get historical stock price data for META and TESLA
meta_dates, meta_prices = get_stock_price('META')
tesla_dates, tesla_prices = get_stock_price('TSLA')

# Plot the stock price change
plt.figure(figsize=(12, 6))
plt.plot(meta_dates, meta_prices, label='META')
plt.plot(tesla_dates, tesla_prices, label='TESLA')
plt.title('META vs TESLA Stock Price Change')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.legend()
plt.xticks(rotation=45)  # Rotate x-axis ticks for better readability
plt.show()