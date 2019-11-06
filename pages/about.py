#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:31 2019

@author: heba
"""

import dash_html_components as html

layout = html.Div(
    className="contents",
    children=[
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
