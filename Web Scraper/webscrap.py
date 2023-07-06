# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:01:03 2023

@author: Danish
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd

tickers = ["AAPL","FB","CSCO","INFY.NS"]
income = {}
balance_sheet  = {}
cash_flow = {}

for ticker in tickers:
    url = "https://finance.yahoo.com/quote/{}/financials?p={}".format(ticker,ticker)
    income_stat = {}
    title = {}
    header = {"User-Agent":"Chrome/114.0.5735.134"}
    page_data = requests.get(url,headers=header)
    page_content = page_data.content
    soup = BeautifulSoup(page_content,"html.parser" )
    table = soup.find_all("div",{"class":"W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
    for t in table:
        heading = t.find_all("div",{"class":"D(tbr) C($primaryColor)"})
        rows = t.find_all("div",{"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for h in heading:
            title[h.get_text(separator="|").split("|")[0]] = h.get_text(separator="|").split("|")[1:]
        for row in rows:
            income_stat[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    temp= pd.DataFrame(income_stat).T
    temp.columns = title["Breakdown"]
    income[ticker] = temp

for ticker in tickers:
    url = "https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(ticker,ticker)
    income_stat = {}
    title = {}
    header = {"User-Agent":"Chrome/114.0.5735.134"}
    page_data = requests.get(url,headers=header)
    page_content = page_data.content
    soup = BeautifulSoup(page_content,"html.parser" )
    table = soup.find_all("div",{"class":"W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
    for t in table:
        heading = t.find_all("div",{"class":"D(tbr) C($primaryColor)"})
        rows = t.find_all("div",{"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for h in heading:
            title[h.get_text(separator="|").split("|")[0]] = h.get_text(separator="|").split("|")[1:]
        for row in rows:
            income_stat[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    temp= pd.DataFrame(income_stat).T
    temp.columns = title["Breakdown"]
    balance_sheet[ticker] = temp
    
for ticker in tickers:
    url = "https://finance.yahoo.com/quote/{}/cash-flow?p={}".format(ticker,ticker)
    income_stat = {}
    title = {}
    header = {"User-Agent":"Chrome/114.0.5735.134"}
    page_data = requests.get(url,headers=header)
    page_content = page_data.content
    soup = BeautifulSoup(page_content,"html.parser" )
    table = soup.find_all("div",{"class":"W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
    for t in table:
        heading = t.find_all("div",{"class":"D(tbr) C($primaryColor)"})
        rows = t.find_all("div",{"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for h in heading:
            title[h.get_text(separator="|").split("|")[0]] = h.get_text(separator="|").split("|")[1:]
        for row in rows:
            income_stat[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    temp= pd.DataFrame(income_stat).T
    temp.columns = title["Breakdown"]
    cash_flow[ticker] = temp
    
#converting dataframe values to numeric
for ticker in tickers:
    for col in income[ticker].columns:
        income[ticker][col] = income[ticker][col].str.replace(',|- ','')
        income[ticker][col] = pd.to_numeric(income[ticker][col], errors = 'coerce')
        cash_flow[ticker][col] = cash_flow[ticker][col].str.replace(',|- ','')
        cash_flow[ticker][col] = pd.to_numeric(cash_flow[ticker][col], errors = 'coerce') 
        if col!="ttm": #yahoo has ttm column for income statement and cashflow statement only
            balance_sheet[ticker][col] = balance_sheet[ticker][col].str.replace(',|- ','')
            balance_sheet[ticker][col] = pd.to_numeric(balance_sheet[ticker][col], errors = 'coerce')
           