#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 06:29:59 2019

@author: heba
"""


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
from app import app


logo_img = 'logo.jpg'
logo_base64 = base64.b64encode(open(logo_img, 'rb').read()).decode('ascii')
    

layout = html.Div(
                id='title',
                className="title",
                children=[
                    html.Table(
                            html.Tr([
                                    html.Td (html.Img(src='data:image/jpg;base64,{}'.format(logo_base64))),
                                    html.Td(html.H1("Inference of Context-Dependent Gene Functions"))])),
                            html.Tr([
                                    html.Td (dcc.Link('Home  ', href='/')),
                                    html.Td (dcc.Link('About  ', href='/about')),
                                    html.Td(dcc.Link('Datasets  ', href='/datasets')),
                                    html.Td(dcc.Link('Citation', href='/citation'))],
                                    style={'padding-left':'20px'}),#Riccardo this is not working
        
                ], style={'backgroundColor':'#eaeaea','margin':'0px','padding':'10px','width':'100%'},
                        
            )