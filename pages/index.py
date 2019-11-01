#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:31 2019

@author: heba
"""

import base64
import os
import re

import pandas

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app


DEFAULT_DATASET_FILE = 'dataset.csv'


dataset = pandas.read_csv(DEFAULT_DATASET_FILE)

dataset_selector = dataset['Dataset'].notnull()
gene_selector = dataset['Gene'].notnull()
functions_selector = dataset['Function(s)'].notnull()
max_rows = 10


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
    # only keep this `max_rows`
    if len(selected) > max_rows:
        selected = selected.loc[0:(max_rows-1)]
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
        html.Div(
            id='intro',
            className="section",
            children=[
                html.P("Use the following input fields to search specific records in the dataset."
                       " The display will update as soon as a value is entered or selected."),
                html.Label("Gene:"),
                dcc.Input(
                    type='text',
                    placeholder="E.g.: DDR1",
                    spellCheck='false',
                    size='20',
                    id='sel-gene',
                ),
                #
                html.Label("Dataset:"),
                selector('Dataset', id='sel-dataset', style={'width': '12em'}),
                #
                html.Label('Keyword(s):'),
                dcc.Input(
                    type='text',
                    placeholder="E.g.: cell cycle",
                    spellCheck='false',
                    size='20',
                    id='sel-functions',
                ),
                #
                html.Label('Max rows per page:'),
                dcc.Input(
                    type='number', min=1,
                    placeholder="E.g.: 100",
                    spellCheck='false',
                    size='10',
                    id='num-rows',
                ),
            ],
        ),
        html.Div(
            id='table-container',
            children=[
                table(),
            ]
        ),
    ],
)


@app.callback(
    Output('table-body', 'children'),
    [
        Input('sel-dataset', 'value'),
        Input('sel-gene', 'value'),
        Input('sel-functions', 'value'),
        Input('sel-functions', 'n_submit'),
        Input('num-rows', 'value'),
    ]
)
def select(dataset_name, gene_name, function_substr, enter_pressed, num_rows):
    global dataset_selector, gene_selector, functions_selector, max_rows

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
    if num_rows is not None:
        max_rows = num_rows
    return table_rows()
