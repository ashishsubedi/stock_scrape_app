
import numpy as np
import pandas as pd


import plotly.graph_objects as go

import os


def EMA(df, period=12, column='Closing Price'):
    return df[column].ewm(span=period, adjust=False).mean()


def MACD(df, low_period=12, high_period=26, signal_period=9, column='Closing Price'):
    EMA_low = EMA(df, period=low_period, column=column)
    EMA_high = EMA(df, period=high_period, column=column)
    MACD_line = EMA_low - EMA_high
    signal_line = MACD_line.ewm(span=signal_period, adjust=False).mean()
    df['MACD'] = MACD_line
    df['Signal'] = signal_line
    return df, MACD_line, signal_line


def plot_MACD_signal(df, macd, signal, volume='Traded Shares', period_text='(12,26,9)', name='', fig=None):
    if not fig:
        fig = go.Figure()

    fig = fig.add_trace(go.Scatter(x=df.index, y=macd,
                        name='MACD', line=dict(color="green"), opacity=0.7),
                        row=2, col=1
                        )
    fig = fig.add_trace(go.Scatter(
        x=df.index, y=signal, name='Signal Line', line=dict(color="red"), opacity=0.7),
        row=2, col=1
    )

    fig.add_trace(go.Scatter(x=df.index, y=np.zeros_like(signal),
                             name='Zero Line', line=dict(color="black"), opacity=0.7),
                  row=2, col=1
                  )
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='MACD Value',row=2,col=1)
    fig.update_layout(
        legend_title="Legend",
     
        transition_duration=500

    )

    return fig


def plot_close_price(df, column='Closing Price', plot_EMA=True, show_buy_sell=True, period_text='(12,26,9)', name='', fig=None):
    if plot_EMA:
        ema10 = EMA(df, period=10, column=column)
        ema100 = EMA(df, period=100, column=column)
    if show_buy_sell:
        buy, sell = buy_sell(df, close=column)

    if not fig:
        fig = go.Figure()
    fig = fig.add_trace(go.Scatter(
        x=df.index, y=df[column], name=column, opacity=0.7))
    if plot_EMA:
        fig = fig.add_trace(go.Scatter(
            x=df.index, y=ema10, name='EMA10', opacity=0.7))
        fig = fig.add_trace(go.Scatter(
            x=df.index, y=ema100, name='EMA100', opacity=0.7))
    if show_buy_sell:
        fig = fig.add_trace(go.Scatter(mode='markers', x=df.index, y=df['Buy'], name='Buy', marker=dict(
            color='green',
            size=10,
            symbol='triangle-up'

        ),
            opacity=0.7),
            row=1, col=1
        )

        fig = fig.add_trace(go.Scatter(mode='markers', x=df.index, y=df['Sell'], name='Sell', marker=dict(
            color='red',
            size=10,
            symbol='triangle-down'

        ),
            opacity=0.7),
            row=1, col=1
        )
 
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Close Price',row=1,col=1)

    return fig


def buy_sell(df, close='Closing Price'):
    buy = []
    sell = []
    flag = -1

    for i in range(len(df)):
        if df['MACD'][i] > df['Signal'][i] and df['MACD'][i] < 0 and flag != 1:
            # MACD crosses signal line from bottom to top below zero line
            flag = 1
            buy.append(df[close][i])
            sell.append(np.nan)
        elif df['MACD'][i] < df['Signal'][i] and df['Signal'][i] > 0 and flag != 0:
            # MACD crosses from top to below above zero line
            flag = 0
            buy.append(np.nan)
            sell.append(df[close][i])
        else:
            buy.append(np.nan)
            sell.append(np.nan)

    df['Buy'] = buy
    df['Sell'] = sell

    return (buy, sell)
