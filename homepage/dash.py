import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable
from dash.dependencies import Input, Output, State

from django_plotly_dash import DjangoDash

import plotly.graph_objects as go

from scrape.models import StockRecord, Stock

import numpy as np
import pandas as pd
import datetime

from django_pandas.io import read_frame


import plotly.graph_objects as go
from plotly.subplots import make_subplots


import os

from scrape.tasks import scrape, symbols_json

from .chart import plot_MACD_signal, plot_close_price, MACD


app = DjangoDash('MACD_plot')   # replaces dash.Dash



app.layout = html.Div([

    html.Div(['Logs:',
            dcc.Textarea(id='logs_area',
                        readOnly=True,
                        style={
                            'width': '100%', 'height': 100}, value=''
                        ),

            ]),
    html.Br(),
    html.Div([

        dcc.Input(id='symbol_name', value='NICA', type='text'),
        html.Button('Get Data', id='submit-val', n_clicks='0'),
    ]),
    dcc.Graph(id='plot-div'),
    html.Div(id="table"),
])


@app.callback(
    Output('plot-div', 'figure'),
    [Input('submit-val', 'n_clicks')],
    state=[
        State('symbol_name', 'value')
    ]
)
def update_figure(_, symbol):
    if not symbol: return 
    symbol = symbol.upper()

    qs = StockRecord.objects.filter(stock__name=symbol)
    df = read_frame(qs, index_col='date')
    df, macd, signal = MACD(df, column='close_price')

    fig = make_subplots(rows=2, cols=1,
    subplot_titles=("Close Price with Buy Sell Signal", "MACD and Signal")
    )

    fig = plot_close_price(df,column='close_price',name=symbol,fig=fig)
    fig = plot_MACD_signal(df,macd,signal,name=symbol,fig=fig)
    fig.update_layout(height=1000)

    return fig


@app.callback(
    Output('table', 'children'),
    [Input('submit-val', 'n_clicks')],
    state=[
        State('symbol_name', 'value')
    ]
)
def update_table(_, symbol):
    if not symbol: return 

    symbol = symbol.upper()


    qs = StockRecord.objects.filter(stock__name=symbol)
    df = read_frame(qs)
    return DataTable(
        id='dash-table',
        columns=[{"name": i, "id": i} for i in df.columns if i != 'id'],
        data=df.to_dict('records'),

    )


@app.callback(

    Output('logs_area', 'value'),

    [
        Input('submit-val', 'n_clicks'),
        Input('logs_area', 'value'),
    ],
    state=[
        State('symbol_name', 'value'),
    ]
)
def update_logs(_, text, symbol):
    if not symbol: 
        new_text = f'[{datetime.datetime.now()}] FAILED - INVALID SYMBOL\n'
        text = new_text + text

        return text

    symbol = symbol.upper()

    if not symbol in symbols_json['symbols']:
        new_text = f'[{datetime.datetime.now()}] FAILED - INVALID SYMBOL\n'
    else:
        new_text = f'[{datetime.datetime.now()}] SUCCESS - {symbol} LOADED\n'

    text = new_text + text

    return text
