import dash_core_components as dcc
import dash_html_components as html

import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import base64
import os
import pytesseract
import pandas as pd
from pdf2image import *
import PIL
import re
from PyPDF3 import PdfFileWriter, PdfFileReader
import io
import datetime

layout1 = html.Div(
    [
        dbc.Row(
            [
            html.H6("Text Summarizer and Paraphraser!")]),
        dbc.Row(
            [dbc.Col(
                [html.Div(
                    dcc.Textarea(
                        id='textarea-state-example',
                        value='Textarea content initialized\nwith multiple lines of text',
                        style={'width': '100%', 'height': 500},
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
            dcc.Link('Home', href='/index'),],
    style={"text-align":"center","verticalAlign":"middle","margin":20})

layout2 = html.Div(
    [
        dbc.Row(
            [
            html.H6("OCR-PDF2CSV!")]),
        dbc.Row(
            [dbc.Col(
                [html.Div([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                        ]), multiple=True,),
                    html.Div(id='output-data-upload'),]
                ),],),
            dbc.Col([
                html.Button("Download CSV", id="btn_csv"),
                dcc.Download(id="download-dataframe-csv"),])
            ]),
        dcc.Link('Home', href='/index')
    ],)