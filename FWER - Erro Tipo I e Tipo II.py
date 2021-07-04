# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 04:36:03 2021

@author: flavi
"""
# Para fazer as análises abaixo precisaremos do Sharpe Ratio Máximo e Mediano (SR*)
# Assimetria e Kurtose, além do número de experimentos independentes (14)
# Número de dias observados é de 1220, são 5 anos com uma frequência de 244 dias

import scipy.stats as ss
import numpy as np
import pandas as pd
import statistics

df = pd.read_excel('C:/Users/flavi/Desktop/CruzamentoMedias.xlsx')
df

# Sharpe Ratio, Assimetria e Kurtose

data = pd.DataFrame()
data['Média'] = df.mean()
data['Desvio Padrão'] = df.std()
data['Sharpe Ratio'] = data['Média']/data['Desvio Padrão']
data['Assimetria'] = df.skew()
data['Kurtose'] = df.kurtosis()

##############################################################################

print(data['Sharpe Ratio'].sort_values())

# Sharpe Ratio Máximo e sua Assimetria e Kurtose

ticket = df['MGLU3.1']

sr = 0.089469
skew_max = ticket.skew()
kurt_max = ticket.kurtosis()

# Sharpe Ratio Anualizado

sr_anual = sr*np.sqrt(244)
sr_anual

# Sharpe Ratio Mediano

sr_ = statistics.median(data['Sharpe Ratio'])
sr_

## anualizado
sr__anual = sr_*np.sqrt(244)
sr__anual


## ERRO TIPO I

# Definindo a z[0]:
    
def getZStat(sr, t, sr_=0, skew = 0, kurt=3):
    z = (sr-sr_)*(t-1)**.5
    z /= (1-skew*sr+(kurt-1)/4.*sr**2)**.5
    return z

z0 = getZStat(sr = sr, t = 1220, sr_ = sr_, skew = skew_max, kurt = kurt_max)


# Taxa de falsos positivos antes da clusterização

def type1Err(z, k=1):
    # false positive rate
    alpha = ss.norm.cdf(-z)
    alpha_k = 1 - (1-alpha)**k # multi-testing correction
    return alpha_k

alpha = type1Err(z = z0, k = 1)

print('Com o valor de', tipo1, 'recusaríamos a hipotese nula e declarariamos que a estratégia é verdadeira' )


# Usando a clusterização com N experimentos independentes

def main0():
    # Numerical example
    t,skew,kurt,k,freq=1220, skew_max , kurt_max , 14 , 244
    sr = sr_anual/freq**.5
    sr_ = sr__anual/freq**.5
    
    z = getZStat(sr, t, sr_ , skew, kurt)
    alpha_k = type1Err(z, k = k)
    print(alpha_k)
    return




## ERRO TIPO II

# Definindo o Theta

def getTheta(sr, t, sr_=0, skew = 0, kurt = 3):
    theta = sr_*(t-1)**.5
    theta /= (1-skew*sr+(kurt - 1)/4.*sr**2)**.5
    return theta

theta = getTheta(sr = sr, t = 1220, sr_ = sr_ , skew = skew_max, kurt = kurt_max )

# Definindo o beta sem clusterização

def type2Err(alpha_k, k, theta):
    # false negative rate
    z = ss.norm.ppf((1 - alpha_k)**(1./k)) # Sidak's correction
    beta = ss.norm.cdf(z-theta)
    return beta

type2Err(alpha_k = 0.1903 , k = 1 , theta = theta)



def main1():
    t,skew,kurt,k,freq=1220, skew_max , kurt_max , 14 , 244
    sr = sr_anual/freq**.5
    sr_ = sr__anual/freq**.5
    
    z = getZStat(sr, t, sr_ , skew, kurt)
    alpha_k = type1Err(z, k=k)
    theta = getTheta(sr, t, sr_, skew, kurt)
    beta = type2Err(alpha_k, k, theta)
    beta_k = beta**k
    print(beta_k)
    return

if __name__=='__main__':main1()
    

