# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 10:09:59 2023

@author: Danish
"""

import yfinance as yf
import datetime as dt
import pandas as pd 
import matplotlib.pyplot as plt
stocks = ["AMZN","MSFT","INTC","GOOG","INFY.NS","3988.HK"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohclv = {}
for tickers in stocks:
    cl_price[tickers] = yf.download(tickers,start,end)["Adj Close"]
    
cl_price.dropna(axis=0,how = 'any',inplace=True)
daily_return = cl_price.pct_change()


fig,ax = plt.subplots()
plt.style.available
plt.style.use("ggplot")
ax.set(title = "Daily Mean Returns",xlabel = "Stocks",ylabel = "Mean Return")
plt.bar(x=daily_return.columns,height=daily_return.mean())