# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 18:23:40 2021

@author: flavi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


petr = yf.download(tickers='YDUQ3.SA', start='2016-01-01', end= '2021-01-01')[['Adj Close']]

# Criando a de 5 dias

SMA5 = pd.DataFrame()
SMA5 = petr.rolling(window=7).mean()

# Criando a de 22 dias 

SMA22 = pd.DataFrame()
SMA22 = petr.rolling(window=30).mean()

data = pd.DataFrame()
data['petr'] = petr['Adj Close']
data['SMA5'] = SMA5['Adj Close']
data['SMA22'] = SMA22['Adj Close']

data['position'] = np.where(data['SMA5'] > data['SMA22'], 1, -1)

data.dropna(inplace = True)

data['returns'] = np.log(data['petr']/ data['petr'].shift(1))
data['strategy'] = data['position'].shift(1)*data['returns'] 

data[['returns', 'strategy']].sum()*100

retornos=data[['strategy']]*100
retornos

retornos.to_excel('BBASE3.xlsx')









