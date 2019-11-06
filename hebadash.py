#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:46:05 2019

@author: heba
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import index, about, citation, datasets, footer, header


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        content = index.layout
    elif pathname == '/datasets':
        content = datasets.layout
    elif pathname == '/citation':
        content = citation.layout
    elif pathname == '/about':
        content = about.layout
    else:
        return '404'
    return header.layout, content, footer.layout

# expose the Flask app object to uWSGI
server = app.server


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
