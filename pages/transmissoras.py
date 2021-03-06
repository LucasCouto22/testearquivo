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

dash.register_page(__name__, path='/')

os.listdir()

df=pd.read_csv('base_transmissoras.csv')

df.head()

dfd=df[['Nome','Tensao','extensao','ano','Empresa','Grupo Controlador']]


with open('transmissoras_agregado.json') as f:
    dist_json = json.load(f)

  
fig2 = px.sunburst(df, path=['ano', 'Empresa','Contrato'])  

fig = px.choropleth_mapbox(
        df, geojson=dist_json,
        locations="Nome", featureidkey="properties.Nome",color='ano',
        center= {"lat":-14.272572694355336,"lon": -51.25567404158474}, zoom=3,
        mapbox_style="carto-positron"
        )
fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        )


df.index
df.rename(columns={'Cigla da Distribuidora':'Sigla'},inplace=True)
df.head()

dfd=df.copy()
del dfd['Unnamed: 0']
del dfd['geometry']


#@app.callback(
#    Output('datatable-interactivity', 'style_data_conditional'),
#    Input('datatable-interactivity', 'selected_columns'),
#)
    

def update_styles(selected_columns):
    return [
        {
        'if': { 'column_id': i },
        'background_color': '#1f2630'
    } for i in selected_columns]

layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
                children=[
                    html.A(
                        html.Img(id="logo", style={'width': '200px'}, src="assets/logo2.png"),
                        href="http://coregmonitor.org/",
                    ),
                    html.A(
                        html.Button("Transmissoras", className="link-button"),
                        href="/",
                    ),
                    html.A(
                        html.Button("Distribuidoras", className="link-button"),
                        href="/distribuidoras",
                    ),
                    html.H4(children="Transmissoras de Energia Vincendas at?? 2030"),
                    html.P(
                        id="description",
                        children="Entra aqui um subtitulo de exemplo para dar uma introdu????o.",
                    ),
                ],
            ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="heatmap-container",
                            children=[
                                dcc.Graph(id='graph_map', figure=fig),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    dcc.Graph(id='graph_sub',figure=fig2),
                    id="graph-container"
                ),
            ],
        ),
        html.Div([
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in dfd.columns
                ],
                data=dfd.to_dict('records'),
                style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'center'
                } for c in ['Date', 'Region']
                ],
            style_data={
                'color': 'black',
                'backgroundColor': 'lightblue',
                'border': '1px solid black',
                'width': "20%",
                'textAlign': 'center'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'lightblue'
                }
            ],
            style_header={
                'backgroundColor': 'lightblue',
                'color': 'black',
                'fontWeight': 'bold',
                'border': '1px solid black',
                'width': "20%",
                'textAlign': 'center'
            },
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10,

            ),

            html.Div(id='datatable-interactivity-container'),

            ],
        ),
    ],
)