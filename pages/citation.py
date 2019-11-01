#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:31 2019

@author: heba
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div(
    className="contents",
    children=[
    html.H2('Citation'),
    
    html.P([
    'If you have used data available through KDML-db.org in your work, please cite the following publication:'
    ]),
    
    html.P(['KDML: a machine-learning framework for inference of multi-scale gene functions from genetic perturbation screens'
    ]),
    
    html.P('Heba Sailem, Jens Rittscher, and Lucas Pelkmans'
    ),
    
    html.P([
    'bioRxiv 761106, doi: https://doi.org/10.1101/761106'
    ]),
])


@app.callback(
    Output('citation', 'children'),
    [Input('citationn', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)