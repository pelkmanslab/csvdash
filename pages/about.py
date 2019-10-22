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

layout = html.Div([
        
    html.H2('About KDML'),
    
    html.P([
    'Characterising context-dependent gene functions is crucial for understanding the genetic bases of health and disease. KDML database provides predictions of context-dependent gene functions based on gene perturbation screens. KDML allows investigating'
    ]),
    html.Div([
    html.Li('Cell-type dependent gene functions (e.g. gene functions in colon versus breast cells'),
    html.Li('Functions associated with certain phenotypes (e.g. nuclear morphology or viability'),
    ]),
    
    html.P('Contact heba.sailem at eng.ox.ac.uk')
])


@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('about', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)