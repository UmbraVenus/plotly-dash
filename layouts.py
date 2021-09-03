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
import dash_uploader as du
import uuid

def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        upload_id=uuid.uuid1(),  # Unique session id
    )

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Index", href="/index")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Summarization and Paraphrasing", href="/sum_para"),
                dbc.DropdownMenuItem("PDF2CSV", href="/ocr"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="AWCA",
    brand_href="#",
    color="Primary",
)

layout1 = html.Div(
    [
        navbar,
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

"""
layout2 = html.Div(
    [
        html.H1("OCR-PDF2CSV"),
        html.H2("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.H2("File List"),
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
        dcc.Link('Home', href='/index'),
    ],
)
"""