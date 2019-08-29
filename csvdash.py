#! /usr/bin/env python3

import argparse
import base64
import os
import re

import pandas

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table as dt
from dash_table.Format import Format, Align


app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://unpkg.com/normalize.css",
        "https://unpkg.com/concrete.css",
    ])

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server


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
    csvfile = open('./dataset.csv')
    debug = True
else:
    csvfile, debug = parse_args()

def format_function_names(fns):
    fns = [fn for fn in fns.split(';') if fn.strip()]
    # return html.Ul(children=[
    #     html.Li(fn) for fn in fns if fn
    # ])
    return ' // '.join(fns)


def init_table():
    df = pandas.read_csv(csvfile)
    df[['Function(s)']] = df['Function(s)'].apply(format_function_names)

    return dt.DataTable(
        id='table',
        data=df.to_dict("rows"),
        columns=[
            # Dataset
            {
                'id': 'Dataset',
                'name': 'Dataset',
                'type': 'text',
            },
            # Gene
            {
                'id': 'Gene',
                'name': 'Gene',
                'type': 'text',
            },
            # Function(s)
            {
                'id': 'Function(s)',
                'name': 'Function(s)',
                'type': 'text',
            },
            # Score
            {
                'id': 'Score',
                'name': 'Score',
                'type': 'numeric',
                'format': Format(precision=5, align=Align.left),
            },
        ],
        # table UI
        sort_action='native',
        filter_action='native',
        page_action='native',
        # table style
        style_cell={
            'padding': '15px',
            'width': 'auto',
            'textAlign': 'center'
        },
        style_header={
            'backgroundColor': 'rgb(200, 200, 200)',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Function(s)'},
                'textAlign': 'left',
                'whiteSpace': 'pre-line',
            },
            {
                'if': {'column_id': 'Score'},
                'textAlign': 'left',
            },
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(230, 230, 230)'
            }
        ],
    )


app.layout = html.Div([
    # html.Div(
    #     id='controls',
    #     children=[
    #        html.Button(
    #             "Print",
    #             id='print-button'
    #         ),
    #     ]
    # ),

    html.Div(
        id='csv-header',
        children=[

            # html.Img(
            #     id='logo',
            #     src='data:image/png;base64,{}'.format(
            #         base64.b64encode(
            #             open('assets/logo.png', 'rb').read()
            #         ).decode()
            #     )
            # ),

            html.Div(
                id='csv-header-text',
                children=[
                    html.H1("CSV Report"),
            ]),

            html.P("""
            Type text in the empty boxes under column names to search / limit
            display to the matching values only.
            """),

            html.P("""
            Click on the small arrows besides column names to sort by that column.
            """),
]),

    html.Div(
        id='csv-table',
        children=init_table()
    ),
])

if __name__ == '__main__':
    app.run_server(debug=debug)
