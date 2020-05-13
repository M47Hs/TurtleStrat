# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:38:06 2020

@author: Mathieu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('ERF.PA.csv', index_col = 'Date', parse_dates=True)

df['Buy']=np.zeros(len(df))
df['Sell']=np.zeros(len(df))
df['RollingMin']=df['Close'].rolling(window=12).min()
df['RollingMax']=df['Close'].rolling(window=12).max()

df.loc[df['Close']<=df['RollingMin'],'Sell']=-1
df.loc[df['Close']>=df['RollingMax'],'Buy']=1

exo = df.copy()
exo['Balance']=np.zeros(len(exo))
exo['Owned']=np.zeros(len(exo))
exo.drop(['High', 'Low','Adj Close','Volume'], axis=1, inplace = True)
exo = exo.dropna()
exo.drop(exo.loc[(exo['Buy']==0)&(exo['Sell']==0),'Buy'].index,axis=0,inplace = True)
exo.drop(exo.loc[(exo['Buy']==0)&(exo['Sell']==0),'Sell'].index,axis=0,inplace = True)
exo = exo.reset_index()
exo.loc[0,'Balance']=1000

for i in range (1,len(exo)):
    if exo.loc[i,'Buy']==1:
        if exo.loc[i-1,'Owned']==0:
            exo.loc[i,'Owned']=exo.loc[i-1,'Balance']/exo.loc[i,'Close']
            exo.loc[i,'Balance']=0
        else:
            exo.loc[i,'Owned']=exo.loc[i-1,'Owned']
            
    elif exo.loc[i,'Sell']==-1:
        if exo.loc[i-1,'Balance']==0:
            exo.loc[i,'Balance']=exo.loc[i-1,'Owned']*exo.loc[i,'Close']
            exo.loc[i,'Owned']=0
        else:
            exo.loc[i,'Balance']=exo.loc[i-1,'Balance']
            
exo_index = exo.copy()
exo_index = exo_index.set_index('Date')
exo_index['Valeur']=np.zeros(len(exo_index))
exo_index['Valeur']=exo_index['Balance']+exo_index['Owned']*exo_index['Close']
plt.figure(figsize=(20,14))
plt.subplot(3,1,1)
df.loc[:,'Close'].rolling(window=28).min().plot() #affiche le minimum avec n jours de lag
df.loc[:,'Close'].rolling(window=28).max().plot() #affiche le maximum avec n jours de lag
df['Close'].plot() #affichage cours en temps réel
plt.legend()
plt.yscale('log')
#data.loc[df.loc['Close']>=]
plt.subplot(3,1,2)
df['Buy'].plot(c='g',label='buy')
df['Sell'].plot(c='r',label='sell')
plt.legend()
plt.subplot(3,1,3)
exo_index['Valeur'].plot(label='Valeur du Compte') #affichage cours en temps réel
plt.legend()
plt.yscale('linear')
plt.show()