#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 06:03:23 2019

@author: heba
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div(
    className="footer",
    children=[
    html.Hr(),
    html.P('The contents of kdml-go.org are available under the Creative Commons Attribution 4.0 International License (CC BY 4.0) with attribution (citation) required.')          
])