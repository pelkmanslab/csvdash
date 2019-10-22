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
        return header.layout, index.layout, footer.layout
    elif pathname == '/datasets':
        return header.layout, datasets.layout, footer.layout
    elif pathname == '/citation':
        return header.layout, citation.layout, footer.layout
    elif pathname == '/about':
        return header.layout, about.layout, footer.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)