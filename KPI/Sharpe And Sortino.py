# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 11:46:57 2023

@author: Danish
Sharpe And Sortino Ratio 
Sharpe = CAGR-Risk_Free_Rate/Volitality i.e. Return-RiskFree_Rate/Std_dev
Sourtino is same just, we just consider negative volatitlty for calculation
"""

import yfinance as yf
import pandas as pd
import numpy as np

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
    n = (len(df))/ 252
    CAGR_Value = (df['Cum_Ret'][-1])**(1/n) - 1
    return CAGR_Value

def Volitality(DF):
    df = DF.copy()
    df['Daily_Ret'] = df['Adj Close'].pct_change()
    vol = df['Daily_Ret'].std() * np.sqrt(252)
    return vol
 
def Sharpe(DF,rf):
    df = DF.copy()
    return (CAGR(df)-rf)/Volitality(df)

def Sortino(DF,rf):
    df = DF.copy()
    df['daily_return'] = df['Adj Close'].pct_change();
    neg_return = np.where(df['daily_return']>0,0,df['daily_return'])
    neg_vol = pd.Series(neg_return[neg_return!=0]).std() * np.sqrt(252)
    return (CAGR(df)-rf)/neg_vol

for ticker in ohlcv:
    print("For {} Sharpe is {} and Sortino is {}".format(ticker,Sharpe(ohlcv[ticker],0.03),Sortino(ohlcv[ticker],0.03)))