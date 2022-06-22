import dash
# import random
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
from shapely import wkt


# --- DEFINIÇÃO DE VARIÁVEIS INICIAIS
# Todas estas variáveis são estáticas

#importar os dados da base de dados

df = pd.read_excel("resources/dados_fichas_areas.xlsx")

# Transformar coluna 'geometry' da df para gdf (coordenadas geopandas para visualização no mapa)
import copy
df2 = copy.copy(df)
df2['geometry'] = df2['geometry'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df2, crs='epsg:3763')
gdf = gdf.to_crs("EPSG:4326")

titulos_tabela_areas = {
    "Ficheiro": "Ficheiro",
    "area_const_anexos": "Anexos",
    "area_total_imp": "Implantação",
    "area_bruta_priv": "Bruta Privativa",
    "area_bruta_dep": "Bruta Dependente"
}

# Contagem das categorias 
freq = {} 
for item in df["Categoria da Obra"]: 
    if (item in freq): 
        freq[item] += 1
    else: 
        freq[item] = 1

from src.Plots_AguedaHousingDashboard import *

# --- DEFINIÇÃO DO LAYOUT
# É estático e cada elemento deverá vir de uma função init

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src="https://gis4cloud.com/sigcs2020-21-fatores-hospitalares-covid/wp-content/uploads/sites/5/2021/01/mcdcs_.png",
            width='53%')
        ], width={'size': 3}),
        dbc.Col([
            html.H1("ÁguedaHousingDashboard",style={'height': '90%', 'textAlign': 'center', "color": "white", "margin-top":30 })
        ], width={'size': 6, 'offset': 0}),
    ],
    style={'height': '15%', 'backgroundColor': '#F7BF4B'},),    
    dbc.Row([
        dbc.Col([
            html.P(
                "\n\n\n", 
                className="text-center",
            ),
            html.P(
                "Categoria da Obra", 
                className="text-center",
                style={"font-size": "%spx" % (TITLE_FONT_SIZE), "font-family":"%s" % (TITLE_FONT_FAMILY), "color": "%s" %(TITLE_FONT_COLOR)}
            ),
            html.Div(
                children = [init_categoria_obra(freq)], 
                id="categoria-obra-div",
            ),
            
            html.Button(
                "Limpar seleção",
                id="clean-sele",
                className="reset-button",
            ),
            ], id="cat-div", width={'size': 3, 'height': 3, 'offset': 0},
        ),
        dbc.Col([
             html.P(
                "\n\n\n", 
                className="text-center",
            ),
            html.P(
                "Informações sobre as áreas", 
                className="text-center",
                style={"font-size": "%spx" % (TITLE_FONT_SIZE), "font-family":"%s" % (TITLE_FONT_FAMILY), "color": "%s" %(TITLE_FONT_COLOR)}
            ),
            html.Div(
                children = [init_tabela_areas(df, titulos_tabela_areas)],
                id ="tabela-areas-div",
                )
            
            ], width={'size': 3, 'height': 3, 'offset': 0}),
        dbc.Col([
            html.P(
                "\n\n\n", 
                className="text-center",
            ),
            html.P(
                "Relação entre o custo e a tipologia", 
                className="text-center",
                style={"font-size": "%spx" % (TITLE_FONT_SIZE), "font-family":"%s" % (TITLE_FONT_FAMILY), "color": "%s" %(TITLE_FONT_COLOR)}
            ),
            html.Div(
                children = [init_custo(df)],
                id ="custo-div",)
            
        ], width={'size': 3, 'height': 3, 'offset': 0}),
        dbc.Col([
            html.P(
                "\n\n\n", 
                className="text-center",
            ),
            html.P(
                "Localização dos pedidos de obra", 
                className="text-center",
                style={"font-size": "%spx" % (TITLE_FONT_SIZE), "font-family":"%s" % (TITLE_FONT_FAMILY), "color": "%s" %(TITLE_FONT_COLOR)}
            ),
            html.Div(
                children = [init_mapa(gdf)],
                id ="mapa-div",),
            
        ], width={'size': 3, 'height': 4, 'offset': 0}),
    ]), 

    dbc.Row([
        
        dbc.Col([
            html.Div(
                children = [init_indice_imper(df)],
                id ="indice-imper-div",)
            
        ], width={'size': 3, 'height': 3, 'offset': 0}),

        dbc.Col([
            html.Div(
                children = [init_area_tip(df)],
                id ="area-tip-div",)
            
        ], width={'size': 3, 'height': 3, 'offset': 0}),
        dbc.Col([
            html.Div(
                children = [init_altura_pisos(df)],
                id ="altura-pisos-div",)
            
        ], width={'size': 3, 'height': 3, 'offset': 0}),
        dbc.Col([
            html.Div(
                children = [init_fracao(df)],
                id ="fracao-div",)
            
        ], width={'size': 3, 'height': 3, 'offset': 0}),
    ]),
    dbc.Row( #footer
    [
        dbc.Button("Meta Informação",
            id="btn_image",
            color="secondary"),
        dcc.Download(id="download-image"),
        html.P("Dissertação de Mestrado: Mafalda Pateo Sousa",style={'textAlign': 'center', "color": "white", "backgroundColor": 'rgb(210, 210, 210)'}),
        html.P("Esta dissertação é realizada no âmbito do projeto DRIVIT-UP (PTDC/GES-URB/31905/2017 - POCI-01-0145-FEDER-031905). O projeto DRIVIT-UP é financiado pela Fundação para a Ciência e Tecnologia com o recurso a fundos do programa Compete2020 do programa Portugal2020, por sua vez apoiados pelo FEDER - Fundo Europeu de Desenvolvimento Regional."),
        
    ]),
    
    ], fluid=True, style={"height": "100vh"})


# --- DEFINIÇÃO DOS CALLBACKS
# Alteram propriedades dos elementos do layout

@app.callback(
    Output("categoria-obra-div", "children"),
    Output("tabela-areas-div", "children"),
    Output("indice-imper-div", "children"),
    Output("custo-div", "children"),
    Output("area-tip-div", "children"),
    Output("altura-pisos-div", "children"),
    Output("fracao-div", "children"),
    Output("mapa-div", "children"),
    [Input("categoria-obra", "clickData"),
    Input("clean-sele", "n_clicks")])
def update_data(clicked_data, n_clicks):

    # Definir seleção
    if clicked_data == None:
        categoria_selecionada = None
        index_selecionado     = None
    else:
        categoria_selecionada = clicked_data['points'][0]['y']
        index_selecionado     = clicked_data['points'][0]['pointIndex']

    return update_categoria_obra(freq, index_selecionado), \
        update_tabela_areas(df, titulos_tabela_areas, categoria_selecionada), \
        update_indice_imper(df, categoria_selecionada), \
        update_custo(df, categoria_selecionada), \
        update_area_tip(df, categoria_selecionada), \
        update_altura_pisos(df, categoria_selecionada), \
        update_fracao(df, categoria_selecionada), \
        update_mapa(gdf, categoria_selecionada)

@app.callback(
    Output("download-image", "data"),
    Input("btn_image", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "resources/Metainformação_dash.pdf"
    )

# Added host for production server    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)