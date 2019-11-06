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
    html.H2('Citation'),

    html.P([
    'If you have used data available through KDML-db.org in your work, please cite the following publication:'
    ]),

    html.A([
        'KDML: a machine-learning framework for inference of multi-scale gene functions from genetic perturbation screens'
    ], href="https://www.biorxiv.org/content/10.1101/761106v1"),

    html.P('Heba Sailem, Jens Rittscher, and Lucas Pelkmans'
    ),

    html.P([
    'bioRxiv 761106, doi: https://doi.org/10.1101/761106'
    ]),
])
