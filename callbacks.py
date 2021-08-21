
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
from awca import summarization, paraphrasing, ocr
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import dash_uploader as du
import uuid
from pathlib import Path

from app import app, application

UPLOAD_DIRECTORY = "./app_uploaded_files/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY,)

du.configure_upload(app, UPLOAD_DIRECTORY)

@application.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "./download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

# sum_para
@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        value = paraphrasing.paraphrase(value)
        return 'Here is the result: \n{}'.format(value)

# ocr =============
def populate_csv(files):
    page_ids = []
    #list of all documents
    page_texts = []
    for open_file in files:
        open_file = open("app_uploaded_files/"+open_file, 'rb')
        page_ids.append(open_file.name)
        inputpdf = PdfFileReader(open_file)
        maxPages = inputpdf.numPages
        image_counter = 1
        for page in range(1, maxPages, 10):
            images = convert_from_path(open_file.name, first_page=page, last_page=min(page + 10 - 1, maxPages))
            for image in images:
                image.save('./page' + str(image_counter) + '.jpg', 'jpeg') 
                image_counter += 1
        filelimit = image_counter - 1
        #list of each document
        individual = []
        # read the images generated, and turn into csv using ocr
        for i in range(1, image_counter):
            filename = "page" + str(i) + ".jpg"
            text = pytesseract.image_to_string(PIL.Image.open(filename))
            text.replace("\n'", " ")
            individual += [text]
            if os.path.isfile(filename):
                os.remove(filename)
            else:    ## Show an error ##
                print("Error: %s file not found" % filename)
        page_texts.append(individual)
        
    csv = pd.DataFrame(data={
        'page_ids': page_ids,
        'page_texts': page_texts
    })
    return csv
"""
def parse_contents(contents, filename):
    return html.Div([
        html.H5(filename),
        html.Hr(),  # horizontal line
    ])
"""

@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("upload-data", "filename"), Input("upload-data", "contents"),Input("btn_csv", "n_clicks"),],prevent_initial_call=True,
)
def update_output(uploaded_filenames, uploaded_file_contents,n_clicks):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    newfile = populate_csv(files)
    if len(files) == 0:
        html.Li("No files yet!")
    else:
        html.Li("Upload Completed")
    return dcc.send_data_frame(newfile.to_csv, "mydf.csv")
    

""""
@app.callback(
    Output('callback-output', 'children'),
    Output("download-dataframe-csv", "data"),
    [Input('upload-data', 'isCompleted'), Input("btn_csv", "n_clicks")],
    [State('upload-data', 'fileNames'),
     State('upload-data', 'upload_id')],
    prevent_initial_call=True,
)
def callback_on_completion(iscompleted, filenames, upload_id, n_clicks):
    if not iscompleted:
        return
    out = []
    if filenames is not None:
        root_folder = Path(UPLOAD_DIRECTORY)

        for filename in filenames:
            file = root_folder / filename
            out.append(file)
            newfile = populate_csv(file)
        children = html.Ul([html.Li(str(x)) for x in out])
        return (children, dcc.send_data_frame(newfile.to_csv, "mydf.csv"))

    return html.Div("No Files Uploaded Yet!"), None

@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("upload-data", "filename"), Input("btn_csv", "n_clicks"),],prevent_initial_call=True,
)
def generate_csv(n_clicks, uploaded_filenames):
    newfile = populate_csv(uploaded_filenames)
    html.H5("Convert Finished")
"""