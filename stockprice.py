import yfinance as yf

import matplotlib.pyplot as plt
import seaborn


#Download stock data then export as CSV
#note: takes a few minutes to fetch data
data_df = yf.download("AAPL", start="2020-12-01", end="2020-12-11")
data_df.to_csv('aapl.csv')


#references:
#https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e