import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, application
from layouts import layout1, layout2
import callbacks
import dash_bootstrap_components as dbc

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



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

layout_index = html.Div([
    dcc.Link('Navigate to "/sum-para"', href='/sum_para'),
    html.Br(),
    dcc.Link('Navigate to "/ocr"', href='/ocr'),
    navbar
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