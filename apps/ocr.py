import dash
import dash_core_components as dcc
import dash_html_components as html
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

from app import app



layout = html.Div(
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

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.Hr(),  # horizontal line
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "mydf.csv")