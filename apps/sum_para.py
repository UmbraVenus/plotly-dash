import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from app import app

layout = html.Div(
    [
        dbc.Row(
            [
            html.H6("Text Summarizer and Paraphraser!")], justify="center",),
        dbc.Row(
            [dbc.Col(
                [html.Div(
                    dcc.Textarea(
                        id='textarea-state-example',
                        value='Textarea content initialized\nwith multiple lines of text',
                        style={'width': '100%', 'height': 600},
                        ),
                    ),
                html.Button(
                    'Submit',
                    id='textarea-state-example-button', n_clicks=0),
                ], align="stretch",),
            dbc.Col(
                html.Div(
                    id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}), align="stretch")
            ], justify="center", style={"margin-top": 20}),
            dcc.Link('Home', href='/index')],
    style={"text-align":"center","verticalAlign":"middle","margin":20})

@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        return 'Here is the result: \n{}'.format(value)