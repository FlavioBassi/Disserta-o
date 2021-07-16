# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 18:23:40 2021

@author: flavi
"""
import numpy as np
import pandas as pd
import yfinance as yf

dataset = pd.read_excel('C:/Users/flavi/Desktop/Dissertação/cotacoes.xlsx',
                       index_col=0, parse_dates = True)

# Retornos logarizados

retorno = np.log(dataset / dataset.shift(1))

# Adicionando as médias móveis

sma1 = dataset.rolling(5).mean()
sma2 = dataset.rolling(22).mean()
ma_x = sma1 - sma2

# Trocando o sinal da posição da estratégia (1 = long / -1 = short)

pos = ma_x.apply(np.sign)

# Retornos diários da estratégia

retorno_strategy = pos.shift(1)*retorno
retorno_strategy.to_excel('Cruzamento_sem_custo5-22.xlsx')

# Adicionando os custos de transação

tc = 0.001 # 0.1%

delta_pos = pos.diff().abs()  # o dia que a estratégia muda de posição

custo_transacao = tc*delta_pos # custo de transação * o dia da mudança

my_rs2 = retorno_strategy - custo_transacao
my_rs2.to_excel('Cruzamento_com_custo5-22.xlsx')

