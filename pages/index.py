#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:31 2019

@author: heba
"""



#! /usr/bin/env python3

import argparse
import base64
import os
import re

import pandas

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
#
#app = dash.Dash(
#    __name__,
##    external_stylesheets=[
##        "https://unpkg.com/normalize.css",
##        "https://codepen.io/chriddyp/pen/bWLwgP.css",
##       ]
#    )
#
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
#
#server = app.server


def parse_args():
    parser = argparse.ArgumentParser(
        description="Launch a Dash app to view a CSV file."
    )

    parser.add_argument(
        "csvfile",
        type=argparse.FileType(mode="r"),
        help="Comma-separated values (CSV) file"
    )

    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="enable debug mode"
    )

    args = parser.parse_args()

    return args.csvfile, args.debug


if 'DASH_APP_NAME' in os.environ:
    csvfile = './dataset.csv'
    debug = True
else:
    csvfile, debug = parse_args()

dataset = pandas.read_csv(csvfile)

dataset_selector = dataset['Dataset'].notnull()
gene_selector = dataset['Gene'].notnull()
functions_selector = dataset['Function(s)'].notnull()

def table():
    return html.Table(
        id='table',
        className="table",
        children=[
            html.Thead(
                id='table-header',
                children=[
                    html.Tr(children=[
                        html.Th(name.title())
                        for name in dataset.columns
                    ])
                ]
            ),
            html.Tbody(
                id='table-body',
                children=table_rows(),
            )
        ],
    )


def table_rows():
    selected = dataset.loc[dataset_selector & gene_selector & functions_selector]
    rows = []
    for n, row in selected.iterrows():
        row_classes = [
            "row-{:d}".format(n+1),
            ("row-odd" if (n % 2) else "row-even"),
        ]
        cols = []
        for k, colname in enumerate(selected.columns):
            col_classes = row_classes[:] + [
                "col-{:d}".format(k),
            ]
            if k == 2:
                # format `Function(s)`
                fns = [fn for fn in row[k].split(';') if fn.strip()]
                content = html.Ul(children=[
                    html.Li(fn) for fn in fns if fn.strip()
                ])
            elif k == 3:
                content = "{:2.5f}".format(row[k])
            else:
                # convert any other column to string
                content = str(row[k])
            cols.append(html.Td(content, className=' '.join(col_classes)))
        rows.append(
            html.Tr(children=cols, className=' '.join(row_classes))
        )
    return rows


def selector(colname, default=None, **kwargs):
    values = list(dataset[colname].unique())
    assert len(values) > 0
    if default is None:
        default = 'any'
    return dcc.Dropdown(
        options=[{
            'label': f"All {colname.lower()}s",
            'value':'any',

        }] + [
            {'label':val, 'value':val} for val in values
        ],
        value=default,
        **kwargs
    )
    
    
    


layout = html.Div(
    className="contents",
    children=[
    html.Table([
    html.Tr([    
    html.Td([
            html.Div(
                    
                id='intro',
                className="section",
                children=[
                    html.Table([
                    html.Tr([
                    html.Td([
                    html.Label("Search"),
                    ]),
                    html.Td([
                    html.Label("Gene:")],style={'text-align':'right'}),
                    html.Td([    
                        dcc.Input(
                        type='text',
                        placeholder="E.g.: DDR1",
                        spellCheck='false',
                        size='20',
                        id='sel-gene',
                        ),
                    ]),                                
                    #
                    html.Td([                   
                    html.Label("Dataset:"),
                    ],style={'text-align':'right'}),
                    html.Td([      
                    selector('Dataset', id='sel-dataset'),
# Riccardo I need to change the width of dataset selector
                    ],style={'width':'60px'}),  

                    #
                    html.Td([  
                    html.Label('Keyword'),
                    ],style={'text-align':'right'}),
                    html.Td([                              
                    dcc.Input(
                        type='text',
                        placeholder="E.g.: cell cycle",
                        spellCheck='false',
                        size='20',
                        id='sel-functions',
                    ),
                    ])
                    #html.Button('Search', id='searchBtn', n_clicks_timestamp=0),
                ],               
            ),
        #]
    ]),
    ]),
    html.Tr([    
     
#    html.Div(
#        id='report',
#        className="container section",
#        children=[
#            html.P("""
#            Click on the small arrows besides column names to sort by that column.
#            """),
            html.Div(
                id='table-container',
                children=[table()],
            ),
#        ]
#    ),
    ]),
])])],style={'width':'100%','text-align':'center'})
])


@app.callback(
    Output('table-body', 'children'),
    [
        Input('sel-dataset', 'value'),
        Input('sel-gene', 'value'),
        Input('sel-functions', 'value'),
        Input('sel-functions', 'n_submit'),
    ]
)
def select(dataset_name, gene_name, function_substr, enter_pressed):
    global dataset_selector, gene_selector, functions_selector

        
    if dataset_name == 'any':
        dataset_selector = dataset['Dataset'].notnull()
    else:
        dataset_selector = (dataset['Dataset'] == dataset_name)
    if gene_name == 'any' or gene_name is None:
        gene_selector = dataset['Gene'].notnull()
    else:
        gene_selector = (dataset['Gene'] == gene_name)
    if enter_pressed and function_substr is not None:
        function_substr = function_substr.strip()
        if function_substr:
            functions_selector = dataset['Function(s)'].str.contains(function_substr)
        else:
            functions_selector = dataset['Function(s)'].notnull()
    return table_rows()
