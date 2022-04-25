## LOOKS FINE

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
""" import dash_bootstrap_components as dbc
 """
import plotly.graph_objects as go
import dash_table
import pandas as pd

from balances import total_balances

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)                       

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
                id='figure-1',
                figure={
                    'data': [
                        go.Indicator(
                            mode="number",
                            value=round(total_balances.usdValue.sum(),2),
                        )
                    ],
                    'layout':
                        go.Layout(
                            title="Portfolio Value (USDT)"
                        )
                }
            )], style={'width': '30%', 'height': '300px',
                       'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='figure-2',
                figure={
                    'data': [
                        go.Indicator(
                            mode="number",
                            value=round(total_balances.btcValue.sum(),3),
                            number={'valueformat': 'g'}
                        )
                    ],
                    'layout':
                        go.Layout(
                            title="Portfolio Value (BTC)"
                        )
                }
            )], style={'width': '30%', 'height': '300px',
                       'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='figure-3',
                figure={
                    'data': [
                        go.Indicator(
                            mode="number",
                            value=round(total_balances.ethValue.sum(),3),
                            number={'valueformat': 'g'}
                        )
                    ],
                    'layout':
                        go.Layout(
                            title="Portfolio Value (ETH)"
                        )
                }
            )], style={'width': '30%', 'height': '300px',
                       'display': 'inline-block'}),

    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='figure-4',
                figure={
                    'data': [
                        go.Pie(
                            labels=total_balances.coin.to_list(),
                            values=total_balances.usdValue.to_list(),
                            hoverinfo="label+percent"
                        )
                    ],
                    'layout':
                        go.Layout(
                            title="Portfolio Distribution (in USDT)"
                        )
                }
            )], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='figure-5',
                figure={
                    'data': [
                        go.Bar(
                            x=total_balances.coin.to_list(),
                            y=total_balances.qty.to_list(),
                            name="Token Quantities For Different Assets",
                        )
                    ],
                    'layout':
                        go.Layout(
                            showlegend=False,
                            title="Tokens distribution"
                        )
                }
            )], style={'width': '50%', 'display': 'inline-block'}),
        dcc.Interval(
            id='1-second-interval',
            interval=1000,  # 1000 milliseconds
            n_intervals=0
        )
    ]),
])


@app.callback(Output('figure-1', 'figure'),
              Output('figure-2', 'figure'),
              Output('figure-3', 'figure'),
              Output('figure-4', 'figure'),
              Output('figure-5', 'figure'),
              Input('1-second-interval', 'n_intervals'))
def update_layout(n):
    figure1 = {
        'data': [
            go.Indicator(
                mode="number",
                value=round(total_balances.usdValue.sum(),2),
            )
        ],
        'layout':
            go.Layout(
                title="Portfolio Value (USDT)"
            )
    }
    figure2 = {
        'data': [
            go.Indicator(
                mode="number",
                value=round(total_balances.btcValue.sum(),3),
                number={'valueformat': 'g'}
            )
        ],
        'layout':
            go.Layout(
                title="Portfolio Value (BTC)"
            )
    }
    figure3 = {
        'data': [
            go.Indicator(
                mode="number",
                value=round(total_balances.ethValue.sum(),3),
                number={'valueformat': 'g'}
            )
        ],
        'layout':
            go.Layout(
                title="Portfolio Value (ETH)"
            )
    }
    figure4 = {
        'data': [
            go.Pie(
                labels=total_balances.coin.to_list(),
                values=total_balances.usdValue.to_list(),
                hoverinfo="label+percent"
            )
        ],
        'layout':
            go.Layout(
                title="Portfolio Distribution (in USDT)"
            )
    }
    figure5 = {
        'data': [
            go.Bar(
                x=total_balances.coin.to_list(),
                y=total_balances.qty.to_list(),
                name="Token Quantities For Different Assets",
            )
        ],
        'layout':
            go.Layout(
                showlegend=False,
                title="Tokens distribution"
            )
    }

    return figure1, figure2, figure3, figure4, figure5


if __name__ == '__main__':
    app.run_server(debug=True)