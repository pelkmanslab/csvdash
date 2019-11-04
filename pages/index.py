#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:31 2019

@author: heba
"""

import base64
import os
import re

import numpy as np
import pandas

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app


DEFAULT_DATASET_FILE = 'dataset.csv'


dataset = pandas.read_csv(DEFAULT_DATASET_FILE, dtype={
    'Dataset': str,
    'Gene': str,
    'Function': str,
    'Confidence': np.float,
})

dataset_selector = dataset['Dataset'].notnull()
gene_selector = dataset['Gene'].notnull()
functions_selector = dataset['Function'].notnull()

sort_by = 'Confidence'
sort_ascending = False

max_rows = 20
num_pages = sum(dataset_selector & gene_selector & functions_selector) // max_rows
current_page = 0


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
    # sort
    selected = selected.sort_values(by=sort_by, ascending=sort_ascending, inplace=False)
    # paginate
    start = max_rows*current_page
    end = start + max_rows
    selected = selected.iloc[start:end]
    # build table row by row
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


def pagination():
    global num_pages, current_page
    return html.Div(
        id='pagination',
        className="pagination",
        style={'text-align': 'left'},
        children=[
            html.Div(
                [
                    html.Label('Go to page:'),
                    html.Button('First', id='first', className='first'),
                    dcc.Input(
                        id='page',
                        type='number',
                        value=(current_page+1),
                        min=1,
                        #max=num_pages,
                        #debounce=True,
                        style={'width': '5em'},
                    ),
                    html.Button('Last', id='last', className='last'),
                ],
                style={
                    'clear': 'left',
                    'float': 'left',
                    'margin-right': '1em',
                },
            ),
            #
            html.Div(
                [
                    html.Label('Max rows per page:'),
                    dcc.Input(
                        id='num-rows',
                        type='number', min=1,
                        debounce=True,
                        placeholder="E.g.: 100",
                        spellCheck='false',
                        size='10',
                    ),
                ],
                style={
                    'clear': 'right',
                    'float': 'left',
                    'margin-right': '1em',
                },
            ),
        ],
    )


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
                html.Div(
                    [
                        html.Label("Gene:"),
                        dcc.Input(
                            id='sel-gene',
                            type='text',
                            placeholder="E.g.: DDR1",
                            spellCheck='false',
                            size='20',
                        ),
                    ],
                    style={
                        'clear': 'left',
                        'float': 'left',
                        'margin-right': '1em',
                    },
                ),
                #
                html.Div(
                    [
                        html.Label("Dataset:"),
                        selector('Dataset', id='sel-dataset', style={'width': '12em'}),
                    ],
                    style={
                        'float': 'left',
                        'margin-right': '1em',
                    },
                ),
                #
                html.Div(
                    [
                        html.Label('Keyword(s):'),
                        dcc.Input(
                            id='sel-functions',
                            type='text',
                            placeholder="E.g.: cell cycle",
                            spellCheck='false',
                            size='20',
                            debounce=True,
                        ),
                    ],
                    style={
                        'float': 'left',
                        'margin-right': '1em',
                    },
                ),
                #
                html.Div(
                    [
                        html.Label("Sort by:"),
                        dcc.Dropdown(
                            id='sort-by',
                            options=[{'label':col, 'value':col} for col in dataset.columns],
                            value='Confidence',
                            style={
                                'width': '10em',
                            },
                        ),
                    ],
                    style={
                        'float': 'left',
                        'margin-right': '1em',
                    },
                ),
                #
                html.Div(
                    [
                        dcc.RadioItems(
                            id='sort-asc',
                            options=[
                                {'label': 'Ascending', 'value': '1'},
                                {'label': 'Descending', 'value': '0'},
                            ],
                            value='0',
                            style={
                                'width': '8em',
                            },
                        ),
                    ],
                    style={
                        'clear': 'right',
                        'float': 'left',
                        'margin-right': '1em',
                    },
                ),
            ],
        ),
        html.Div(
            id='table-container',
            children=[
                table(),
                html.Hr(),
                pagination(),
            ],
            style={
                'clear': 'both',
            },
        ),
    ],
)


goto_first_clicked_last = 0
goto_last_clicked_last = 0

@app.callback(
    [
        Output('table-body', 'children')
    ],
    [
        Input('sel-dataset', 'value'),
        Input('sel-gene', 'value'),
        Input('sel-functions', 'value'),
        Input('sel-functions', 'n_submit'),
        # sorting
        Input('sort-by', 'value'),
        Input('sort-asc', 'value'),
        # pagination
        Input('num-rows', 'value'),
        Input('page', 'value'),
        Input('first', 'n_clicks_timestamp'),
        Input('last', 'n_clicks_timestamp'),
    ]
)
def select(dataset_name, gene_name, function_substr, enter_pressed,
           new_sort_by, new_sort_ascending,
           new_max_rows, page, goto_first_clicked, goto_last_clicked):
    global dataset_selector, gene_selector, functions_selector, \
        sort_by, sort_ascending, \
        max_rows, current_page, num_pages, \
        goto_first_clicked_last, goto_last_clicked_last

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
            functions_selector = dataset['Function'].str.contains(function_substr)
        else:
            functions_selector = dataset['Function'].notnull()

    if new_sort_by is not None:
        sort_by = new_sort_by
    if new_sort_ascending is not None:
        sort_ascending = (new_sort_ascending == '1')

    if new_max_rows is not None:
        max_rows = new_max_rows
    if page is not None:
        current_page = page-1
    num_rows = sum(dataset_selector & gene_selector & functions_selector)
    num_pages = num_rows // max_rows
    if num_pages <= current_page:
        current_page = num_pages-1
    if goto_first_clicked is not None and goto_first_clicked > goto_first_clicked_last:
        goto_first_clicked_last = goto_first_clicked
        current_page = 0
    if goto_last_clicked is not None and goto_last_clicked > goto_last_clicked_last:
        goto_last_clicked_last = goto_last_clicked
        current_page = num_pages-1
    # need to return a tuple even if it's just 1 element
    return (table_rows(),)
