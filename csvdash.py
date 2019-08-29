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


app = dash.Dash(__name__)

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


def init_table():
    df = pandas.read_csv(csvfile)
    return dt.DataTable(
        id='table',
        sort_action='native',
        filter_action='native',
        row_deletable=True,
        style_cell={
            'padding': '15px',
            'width': 'auto',
            'textAlign': 'center'
        },
        style_cell_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#f9f9f9'
            }
        ],
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows")
    )


app.layout = html.Div([
    html.Div(
        id='controls',
        children=[
           html.Button(
                "Print",
                id='csv-print'
            ),
        ]
    ),

    html.Div(
        id='frontpage',
        className='page',
        children=[
            html.Div(id='csv-header', children=[

            # html.Img(
            #     id='csv-logo',
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
                ])
            ])
        ]
    ),

    html.Div(className='section', children=[
            html.Div(
                className='section-title',
                children="CSV well"
            ),

            html.Div(
                className='page',
                children=[
                    html.Div(
                        id='csv-table',
                        children=init_table()
                    ),
                    html.Div(
                        id='csv-table-print'
                    )]
            )
    ]),
])


@app.callback(
    Output('csv-table-print', 'children'),
    [Input('table', 'data')]
)
def update_table_print(data):
    colwidths = {
        'mnemonic': '100px',
        'descr': '300px',
        'unit': '25px',
        'value': '300px'
    }
    tables_list = []
    num_tables = int(len(data)/34) + 1 # 34 rows max per page
    for i in range(num_tables):
        table_rows = []
        for j in range(34):
            if i*34 + j >= len(data):
                break
            table_rows.append(html.Tr([
                html.Td(
                    data[i*34 + j][key]
                ) for key in data[0].keys()]))
        table_rows.insert(0, html.Tr([
            html.Th(
                key.title(),
                style={'width': colwidths[key]}
            ) for key in data[0].keys()]))
        tables_list.append(html.Div(className='tablepage', children=html.Table(table_rows)))
    return tables_list


if __name__ == '__main__':
    app.run_server(debug=debug)
