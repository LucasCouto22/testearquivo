from dash import Dash,html,dcc,Input,Output,callback_context,dash_table, dependencies
import plotly.express as px
import pandas as pd
import json
import os
import pathlib
import flask 
import dash_bootstrap_components as dbc
from waitress import serve
import plotly.express as px 
import dash


flask_server = flask.Flask(__name__)
app = Dash(__name__,server=flask_server, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
	dash.page_container
])

app.title = 'CeriLab'
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)  # Atualiza a página automaticamente com modificações do código fonte
