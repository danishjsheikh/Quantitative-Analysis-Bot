# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 12:59:19 2023

@author: Danish
Max DrawDown And Calmar Ratio
Max DrawDown Is Maximum Difference Between Highihest High Followed By Lowest Low 
Calmar Ratio Is CAGR/Max DrawDown
"""

import yfinance as yf


tickers = ["AMZN","GOOG","MSFT","JPPOWER.NS"]

ohlcv = {}

for ticker in tickers:
    temp = yf.download(ticker,period = '1y',interval = '1d')
    temp.dropna(how = 'any',inplace = True)
    ohlcv[ticker] = temp
 
    def CAGR(DF):
        df = DF.copy()
        df['Daily_Ret'] = df['Adj Close'].pct_change()
        df['Cum_Ret'] = (1+df['Daily_Ret']).cumprod()
        n = (len(df))/ 245
        CAGR_Value = (df['Cum_Ret'][-1])**(1/n) - 1
        return CAGR_Value
    
def Max_DrawDown(DF):
    df = DF.copy()
    df['daily_return'] = df['Adj Close'].pct_change()
    df['Cum_ret'] = (1 + df['daily_return']).cumprod()
    df['Cum_roll_max'] = df['Cum_ret'].cummax()
    df['Draw_Down'] = df['Cum_roll_max']-df["Cum_ret"]
    return (df['Draw_Down']/df['Cum_roll_max']).max()

def Calmar(DF):
    df = DF.copy()
    return CAGR(df)/Max_DrawDown(df)
    

for ticker in ohlcv:
    print("For {} \nMax Draw Down is {} \nCalmar Ratio is {}".format(ticker,Max_DrawDown(ohlcv[ticker]),Calmar(ohlcv[ticker]))) 
          

