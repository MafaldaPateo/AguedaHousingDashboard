from string import whitespace
# import dash_core_components as dcc
from dash import dcc
import dash
import plotly.express as px

from src.AguedaHousingDashoard_settings import *

# --- CATEGORIA OBRAS

def init_categoria_obra(freq):

    return dcc.Graph(
        figure={
            'data': [{
                'type': "bar",
                'y': list(freq.keys()),
                'x': list(freq.values()),
                'marker': {"color": "#FFFFFF"},
                'orientation': "h",
                'selectedpoints': [None],
                'selected': {"marker": {"opacity": 1, "color": "#F7BF4B"}},
                'unselected': {"marker": {"opacity": 0.2, "color": "#F7BF4B"}},
                'showlegend': False,
                'hovertemplate': "%{x:,.0}<extra></extra>",
                # 'style':{'width': '50%', 'height': '50%'},
            }], 
            'layout': {
                'template': {"layout": {"paper_bgcolor": "#FFFFFF", "plot_bgcolor": "#FFFFFF"}},
                'xaxis': {"visible": True, 'title': "Número de fichas"},
                'yaxis': {"visible": True},
                'margin': {'t': 0, 'r': 0},
                'height': 250,

                # 'clickmode': 'event+select',
            },
        },
        id='categoria-obra'
    )


def update_categoria_obra(freq, sele):

    fig = init_categoria_obra(freq)

    # Update da seleção do gráfico "Categoria_Obras"
    fig.figure['data'][0]['selectedpoints'] = [sele]

    return fig


# --- TABELA AREAS


def init_tabela_areas(df, titulos_tabela_areas):
    cond = []
     
    fig = dash.dash_table.DataTable(
        data=df.to_dict('records'),
        sort_action='native',
        columns=[
            {'name': titulos_tabela_areas[i], 'id': i} for i in df.columns if i in titulos_tabela_areas.keys()
        ],
        style_data_conditional = cond,
        style_header={ 'background_color': '#F7BF4B', "opacity": '0.7' },
        style_cell = {
            'font_size': '9px',
            'text_align': 'center',
            'whiteSpace': 'normal'},
        fixed_rows={'headers': True}, 
        id='tabela-areas')


 
    return fig



def update_tabela_areas(df, titulos_tabela_areas, sele):

    fig = init_tabela_areas(df, titulos_tabela_areas)

    sele_ids = df[df['Categoria da Obra'] == sele].index

    if sele != None:
        fig.style_data_conditional = [
            {
                'if': {
                    'row_index': sele_ids
                },
                'backgroundColor': '#F7BF4B',
                'color': 'white'
                
            }
        ]

    return fig



# --- ÍNDICE IMPERMEABILIZAÇÃO


def init_indice_imper(df):
    return dcc.Graph(
    figure={
        'data': [{
            'type': "box",
            'x': list(df["indice_imper"]),
            'name': "",
            'marker': {"color": "#F7BF4B"},
            'orientation': "h",
            'selectedpoints': [None],
            'selected': {"marker": {"opacity": 1, "color": "#F7BF4B", 'size': '10'}},
            'unselected': {"marker": {"opacity": 0.5, "color": "#000000"}},
            'showlegend': False,
            'hovertemplate': None,
            'boxpoints': 'all',            
            'jitter':0.0,
        }],
        'layout': {
            'template': {"layout": {"paper_bgcolor": "#FFFFFF", "plot_bgcolor": "#FFFFFF"}},
            'xaxis': {"visible": True},
            'yaxis': {"visible": False},
            'title': {
                "text": 'Índice de Impermeabilização',
                "font": {
                    "size": TITLE_FONT_SIZE,
                    "family": TITLE_FONT_FAMILY,
                    "color": TITLE_FONT_COLOR,
                }
            },
            'height': 350,
    
            # 'clickmode': 'event+select',
        },
    },
    id='indice-imper'
    )
    

def update_indice_imper(df, sele):
    fig = init_indice_imper(df)
    
    # indices que correspondem ao sele identificado
    lista_selecao = []
    for (indice,i) in enumerate(df["Categoria da Obra"]):
        if i == sele:
            lista_selecao.append(indice)

    # Update da seleção do gráfico "Categoria_Obras"
    fig.figure['data'][0]['selectedpoints'] = lista_selecao

    return fig


# --- RELAÇÃO DA ESTIMATIVA DE CUSTO E DA TIPOLOGIA

def init_custo(df):
    return dcc.Graph(
    figure={
        'data': [{
            'type': "scatter",
            'x': list(df["tip"]),
            'y': list(df["estimativa_obra"]),
            'marker': {"color": "#FFFFFF"},
            'orientation': "h",
            'selectedpoints': [None],
            'selected': {"marker": {"opacity": 1, "color": "#F7BF4B", 'size': '10'}},
            'unselected': {"marker": {"opacity": 0.5, "color": "#000000"}},
            'showlegend': False,
            'hovertemplate': None,
        }],
        'layout': {
            'template': {"layout": {"paper_bgcolor": "#FFFFFF", "plot_bgcolor": "#FFFFFF"}},
            'xaxis': {"visible": True, 'title': 'Tipologia'},
            'yaxis': {"visible": True, 'title': 'Estimativa do custo (€)'},
            'margin': {'t': 0, 'r': 0},
            'height': 250,
           
            # 'clickmode': 'event+select',
        },
    },
    id='custo-tip'
    )

def update_custo(df, sele):
    fig = init_custo(df)

    # indices que correspondem ao sele identificado
    lista_selecao = []

    for (indice,i) in enumerate(df["Categoria da Obra"]):
        if i == sele:
            lista_selecao.append(indice)

    # Update da seleção do gráfico "Categoria_Obras"
    fig.figure['data'][0]['selectedpoints'] = lista_selecao

    return fig


# --- RELAÇÃO ENTRE A ÁREA DE CONSTRUÇÃO E A TIPOLOGIA

def init_area_tip(df):
    fig = dcc.Graph(
        figure={
            'data': [{
                'type': "scatter",
                'x': list(df["area_total_const"]),
                'y': list(df["tip"]),
                'marker': {"color": "#FFFFFF"},
                'orientation': "h",
                'selectedpoints': [None],
                'selected': {"marker": {"opacity": 1, "color": "#F7BF4B", 'size': '10'}},
                'unselected': {"marker": {"opacity": 0.5, "color": "#000000"}},
                'showlegend': False,
                'hovertemplate': None,
            }],
            'layout': {
                'template': {"layout": {"paper_bgcolor": "#FFFFFF", "plot_bgcolor": "#FFFFFF"}},
                'xaxis': {"visible": True, 'title':'Área Total de Construção (m2)' },
                'yaxis': {"visible": True, 'title': 'Tipologia'},
                'title': {
                    "text": 'Relação entre a área de construção e a tipologia',
                    "font": {
                        "size": TITLE_FONT_SIZE,
                        "family": TITLE_FONT_FAMILY,
                        "color": TITLE_FONT_COLOR,
                    }
                },
                'height': 350,
                # 'clickmode': 'event+select',
            },
        },
        id='area-tip'
    )

    return fig


def update_area_tip(df, sele):
    fig = init_area_tip(df)

    # indices que correspondem ao sele identificado
    lista_selecao = []

    for (indice,i) in enumerate(df["Categoria da Obra"]):
        if i == sele:
            lista_selecao.append(indice)

    # Update da seleção do gráfico "Categoria_Obras"
    fig.figure['data'][0]['selectedpoints'] = lista_selecao

    return fig



# --- RELAÇÃO ENTRE A ALTURA E OS PISOS

def init_altura_pisos(df):
    return dcc.Graph(
    figure={
        'data': [{
            'type': "scatter",
            'x': list(df["altura"]),
            'y': list(df["n_pisos"]),
            'marker': {"color": "#FFFFFF"},
            'orientation': "h",
            'selectedpoints': [None],
            'selected': {"marker": {"opacity": 1, "color": "#F7BF4B", 'size': '10'}},
            'unselected': {"marker": {"opacity": 0.5, "color": "#000000"}},
            'showlegend': False,
            'hovertemplate': None,
        }],
        'layout': {
            'template': {"layout": {"paper_bgcolor": "#FFFFFF", "plot_bgcolor": "#FFFFFF"}},
            'xaxis': {"visible": True, 'title': 'Altura'},
            'yaxis': {"visible": True, 'title': 'Número de pisos'},
            'title': {
                "text": 'Relação entre a altura e o número de pisos',
                "font": {
                    "size": TITLE_FONT_SIZE,
                    "family": TITLE_FONT_FAMILY,
                    "color": TITLE_FONT_COLOR,
                }
            },
            'height': 350,
            # 'clickmode': 'event+select',
        },
    },
    id='altura-pisos'
    )


def update_altura_pisos(df, sele):
    fig = init_altura_pisos(df)

    # indices que correspondem ao sele identificado
    lista_selecao = []

    for (indice,i) in enumerate(df["Categoria da Obra"]):
        if i == sele:
            lista_selecao.append(indice)

    # Update da seleção do gráfico "Categoria_Obras"
    fig.figure['data'][0]['selectedpoints'] = lista_selecao

    return fig


# --- NÚMERO DE FRAÇÃO


def init_fracao(df):
    return dcc.Graph(
    figure={
        'data': [{
            'type': "bar",
            'x': list(df["n_fracoes"]),
            'y': list(df["Ficheiro"]),
            'marker': {"color": "#FFFFFF"},
            'orientation': "h",
            'selectedpoints': [None],
            'selected': {"marker": {"opacity": 1, "color": "#F7BF4B"}},
            'unselected': {"marker": {"opacity": 0.2, "color": "#F7BF4B"}},
            'showlegend': False,
            'hovertemplate': "%{x:,.0}<extra></extra>",
        }],
        'layout': {
            'template': {"layout": {"paper_bgcolor": "#FFFFFF", "plot_bgcolor": "#FFFFFF"}},
            'xaxis': {"visible": True, 'title': 'Número de frações'},
            'yaxis': {"visible": True, 'title': 'Ficheiro'},
            'title': {
                "text": 'Número de frações por pedido de licenciamento',
                "font": {
                    "size": TITLE_FONT_SIZE,
                    "family": TITLE_FONT_FAMILY,
                    "color": TITLE_FONT_COLOR,
                }
            },
            'height': 350,
            # 'clickmode': 'event+select',
        },
    },
    id='fracao'
    )

def update_fracao(df, sele):
    fig = init_fracao(df)

    # indices que correspondem ao sele identificado
    lista_selecao = []

    for (indice,i) in enumerate(df["Categoria da Obra"]):
        if i == sele:
            lista_selecao.append(indice)

    # Update da seleção do gráfico "Categoria_Obras"
    fig.figure['data'][0]['selectedpoints'] = lista_selecao

    return fig



# --- MAPA

def init_mapa(gdf):

    px.set_mapbox_access_token("pk.eyJ1IjoibWFmYWxkYXBhdGVvIiwiYSI6ImNsM2p4NGFqbzBjeXkzZHBpdDl6cDNwdTYifQ.xybg_XIo7KMjHrSWiyFd2A")
    mapa = px.scatter_mapbox(gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        hover_name="Ficheiro",
        hover_data=["address", "Freguesia_x"],
        zoom=9, 
        height=300,
    
        color_discrete_sequence= ["#808080"])

    mapa.layout.showlegend=False
    mapa.update_layout(margin=dict(t=0))

    return dcc.Graph(
        figure=mapa,
        id='mapa'
    )

def update_mapa(gdf, sele):

    lista_selecao = []

    for i in gdf["Categoria da Obra"]:
        if i == sele:
            lista_selecao.append('SELE')
        else:
            lista_selecao.append('NO_SELE')

    gdf['sele'] = lista_selecao

    px.set_mapbox_access_token("pk.eyJ1IjoibWFmYWxkYXBhdGVvIiwiYSI6ImNsM2p4NGFqbzBjeXkzZHBpdDl6cDNwdTYifQ.xybg_XIo7KMjHrSWiyFd2A")
    mapa = px.scatter_mapbox(gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        hover_name="Ficheiro",
        hover_data=["address", "Freguesia_x"],
        zoom=9,
        height=300,
        color = 'sele',
        color_discrete_map={"SELE": "#F7BF4B", "NO_SELE" : "#808080"})

    mapa.layout.showlegend=False
    mapa.update_layout(margin=dict(t=0, l=5, r=5))

    return dcc.Graph(
        figure=mapa,
        id='mapa'
    )