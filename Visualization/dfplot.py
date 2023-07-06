# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:06:20 2023

@author: Danish
"""

import yfinance as yf
import datetime as dt
import pandas as pd 
stocks = ["AMZN","MSFT","INTC","GOOG","INFY.NS","3988.HK"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohclv = {}
for tickers in stocks:
    cl_price[tickers] = yf.download(tickers,start,end)["Adj Close"]
    
cl_price.dropna(axis=0,how = 'any',inplace=True)

cl_price.plot(subplots = True,layout = (3,2),title = 'Closed Prices')
cl_price.mean()
cl_price.std()
cl_price.median()
cl_price.describe()
cl_price.head()
cl_price.tail(9)
daily_return = cl_price.pct_change()
#daily_return cl_price/cl_price.shift(1) - 1
daily_return.mean()
daily_return.std()

daily_return.plot(subplots = True,layout = (3,2),title = 'Closed Prices')

df = daily_return.rolling(window = 10).mean()
df2 = daily_return.ewm(com =10,min_periods=10).mean()

(1+daily_return).cumprod().plot() #Cummilative Prod