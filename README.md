# HebaDash

'LAStoDash` is simple [Dash](https://plot.ly/products/dash)
application that takes a CSV file with 4 columns and shows the content
in a web page, allowing simple search/filtering.

The CSV dataset *must* have the following format (example):

```csv
Dataset,Gene,Function(s),Score
MCF7,DDR1,early endosome;,0.142973749
MCF7,DDR1,endopeptidase inhibitor activity;negative regulation of endopeptidase activity;peptidase inhibitor activity;peptidase regulator ... <Preview truncated at 128 characters>,0.207076131
MCF7,DDR1,angiogenesis;blood vessel morphogenesis;,0.223826555
HCT116,GDI1,positive regulation of angiogenesis;positive regulation of vasculature development;,0.090687684
HCT116,GDI1,protein polyubiquitination;,0.090705461
```

Requires Python 3.6+, won't run in earlier versions of Python.


## Installation

```
$ git clone https://github.com/pelkmanslab/hebadash.git
$ cd hebadash
$ pip3 install -r requirements.txt
```

## Usage

```
$ ./hebadash.py --debug dataset.csv
Running on http://127.0.0.1:8050/
Debugger PIN: 187-833-118
 * Serving Flask app "hebadash" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
Running on http://127.0.0.1:8050/
Debugger PIN: 909-647-004
```
