# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 12:02:13 2021

@author: flavi
"""
import numpy as np
import pandas as pd
import yfinance as yf


ibovurl = "http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=ibrx&idioma=pt-br"
ibrx = pd.read_html(ibovurl)
# Selecionando apenas a columa dos tickers 
tickers = ibrx[0][0:]['Código'].tolist()
tickers.remove('Quantidade Teórica Total  Redutor')
# Adicionando .SA em todas as ações
for i in range(0, len(tickers)):
    tickers[i] = tickers[i] + '.SA'            
    # Buscando no yahoo finance o preço de fechamento ajustado
dataset = yf.download(tickers = tickers, start = '2015-10-01', end = '2021-01-01')['Adj Close']
missing_fractions = dataset.isnull().mean().sort_values(ascending=False)
missing_fractions.head(10)
drop_list = sorted(list(missing_fractions[missing_fractions > 0.40].index))
dataset.drop(labels=drop_list, axis=1, inplace=True)
dataset=dataset.fillna(method='ffill')

dataset.to_csv('output.csv')