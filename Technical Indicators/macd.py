# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 19:28:58 2023

@author: Danish
"""

import yfinance as yf

tickers= ['AMZN','GOOG','MSFT']

ochlv_data = { }

for ticker in tickers:
        temp = yf.download(ticker, interval ='15m',period = '1mo' )
        temp.dropna(inplace=True, how = 'any')
        ochlv_data[ticker] = temp
df = ochlv_data['AMZN']        
def MACD(DF,a=12,b=26,c=9):             #a is fast moving average, b is slow moving average, and c is moving average of botn a and b
    df = DF.copy() #Creating Copy Of Data Frame
    df['ma_fast'] = df['Adj Close'].ewm(span=a, min_periods = a).mean()
    df['ma_slow'] = df['Adj Close'].ewm(span=b, min_periods = b).mean()
    df['macd'] = df['ma_fast'] -  df['ma_slow']
    df["signal"] = df['macd'].ewm(span=c, min_periods = c).mean()
    return df.loc[:,["macd",'signal']]

for ticker in ochlv_data:
    ochlv_data[ticker][["macd","signal"]] = MACD(ochlv_data[ticker])
    