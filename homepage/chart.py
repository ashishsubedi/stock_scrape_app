
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import os
def EMA(df, period = 12,column='Closing Price'):
    return df[column].ewm(span=period,adjust=False).mean()

def MACD(df, low_period=12,high_period=26,signal_period=9,column='Closing Price'):
    EMA_low = EMA(df,period=low_period,column=column)
    EMA_high = EMA(df,period=high_period,column=column)
    MACD_line= EMA_low - EMA_high
    signal_line = MACD_line.ewm(span=signal_period,adjust=False).mean()
    df['MACD'] = MACD_line
    df['Signal'] = signal_line
    return df,MACD_line,signal_line



def plot_MACD_signal(df,macd,signal,use_plotly=True,volume='Traded Shares',period_text='(12,26,9)',name=''):
    if use_plotly:
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x=df.index,y=macd,name='MACD',line=dict(color="green"), opacity=0.7))
        fig = fig.add_trace(go.Scatter(x=df.index,y=signal,name='Signal Line',line=dict(color="red"), opacity=0.7))
        fig.update_layout(
            title={
                'text': "MACD and Signal of ->"+ name+ period_text},
            legend_title="Legend",
            xaxis_title='Date',
            yaxis_title='MACD Value', 
        )
        fig.add_trace(go.Scatter(x=df.index,y=np.zeros_like(signal),name='Zero Line',line=dict(color="black"), opacity=0.7))
        # fig.add_trace(go.Histogram(x=df.index,y=df[volume],name='Volume',opacity=0.7))

        

        fig.show()
        



def buy_sell(df,close='Closing Price'):
    buy = []
    sell = []
    flag = -1

    for i in range(len(df)):
        if df['MACD'][i]>df['Signal'][i] and df['MACD'][i]<0  and flag != 1:
            #MACD crosses signal line from bottom to top below zero line
            flag = 1
            buy.append(df[close][i])
            sell.append(np.nan)
        elif df['MACD'][i] < df['Signal'][i] and df['Signal'][i]>0  and flag!= 0:
            #MACD crosses from top to below above zero line
            flag=0
            buy.append(np.nan)
            sell.append(df[close][i])
        else:
            buy.append(np.nan)
            sell.append(np.nan)
            
    df['Buy'] = buy
    df['Sell'] = sell

    return (buy,sell)