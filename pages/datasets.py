#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:45:31 2019

@author: heba
"""

import dash_core_components as dcc
import dash_html_components as html


layout = html.Div(
className='contents',
children=[
html.H2('Datasets'),
html.H3('HCT116'),
html.P([
    dcc.Markdown('''**Readout:** cell morphology, microenvironment, and rotavirus infection'''),
    dcc.Markdown('''**Tissue type:** colorectal cancer'''),
    dcc.Markdown('''**Description:** An image-based high-throughput RNAi screens was performed in human HCT 116 cells. It is composed of 18,240 gene knockdowns and is performed in duplicate. The cells were stained with DAPI and rotavirus-expressed viral protein. For each single cell, features quantifying morphology, microenvironment, and infection in HCT116 colorectal cancer cells were extracted. These features were aggregated for each gene resulting in 1,719 features per gene perturbation[1].'''),
]),

html.H3('CRISPR'),
html.P([
dcc.Markdown('''**Readout:** Viability'''),
dcc.Markdown('''**Tissue type:** 12 tissue types (cancer)'''),
dcc.Markdown('''**Description**: A curated dataset consisting of 80 genome-scale CRISPR/Cas9 screens measuring viability in 60 different human cancer cell lines from 12 tissue types. 15,055 gene perturbations are shared across all the screens. The data was generated by different laboratories and integrated by Rauscher et al. to correct for various technical issues2''')
]),



html.H3('MCF7'),
html.P([
dcc.Markdown('''**Readout:** transcriptome'''),
dcc.Markdown('''**Tissue type:** Breast cancer'''),
dcc.Markdown('''**Description:** An siRNA screen by the Broad Institute measuring the expression levels of 3,287 genes.'''),
])
])
