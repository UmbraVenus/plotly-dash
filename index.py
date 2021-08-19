import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import layout1, layout2
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    dcc.Link('Navigate to "/sum-para"', href='/sum_para'),
    html.Br(),
    dcc.Link('Navigate to "/ocr"', href='/ocr'),
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/sum_para':
         return layout1
    elif pathname == '/ocr':
         return layout2
    else:
        return layout_index

if __name__ == '__main__':
    app.run_server(debug=True)