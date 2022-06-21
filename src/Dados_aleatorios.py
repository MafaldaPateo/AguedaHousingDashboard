# Para fazer os mapas e dashboard
import plotly.express as px
import json
import dash
from dash import dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import dash_labs as dl
from dash import Dash, dcc, html
import pandas as pd
import geopandas as gpd


# Para criar os valores aleatórios
import random
from shapely.geometry import Polygon, Point

# Utilizamos a biblioteca random para criar valores aleatórios dentro de um range

def tipo_aleatoria():
    """
    Esta função calcula um valor aleatório para a tipologia.
    """
    tip_aleatoria = random.randint(0,5)
    return tip_aleatoria


def pisos(tip_aleatoria):
    """
    Esta função calcula o valor para o número de pisos em função do valor da tipologia. No caso de a tipologia ser menor que 2, 
    então o número de pisos será 1. No caso de a tipologia ser igual ou maior que 2 então o valor do piso será um valor entre 1 e 3 (inclusive). 
    """
    if tip_aleatoria < 2:
        piso_aleatorio = 1
        return piso_aleatorio
    elif tip_aleatoria >= 2:
        piso_aleatorio = random.randint(1,3)
        return piso_aleatorio 


def pisos_local(piso_aleatorio):
    """
    Esta função calcula o valor dos pisos acima e abaixo da cota de soleira, em função do valor do número de pisos. 
    No caso de o número de pisos ser igual a 1, então o número de pisos acima é 1 e o abaixo é 0. 
    No caso de o número de pisos ser 2, o número de pisos acima é um 1 ou 2 e abaixo é 0 ou 1 (sendo que a soma terá de ser 2). 
    Por fim, no caso de o número de pisos ser 3, o número de pisos acima será entre 1 e 3 e o abaixo um valor entre 1 e 2 (sendo que a soma terá de ser 3).
    """
    if piso_aleatorio == 1:
        pisos_acima_aleatorio = 1
        pisos_abaixo_aleatorio = 0
        return pisos_acima_aleatorio, pisos_abaixo_aleatorio
    elif piso_aleatorio == 2:
        pisos_acima_aleatorio = random.randint(1,2)
        if pisos_acima_aleatorio == 2:
            pisos_abaixo_aleatorio = 0
        else:
            pisos_abaixo_aleatorio = random.randint(0,1)
        return pisos_acima_aleatorio, pisos_abaixo_aleatorio
    elif piso_aleatorio == 3:
        pisos_acima_aleatorio = random.randint(1,3)
        if pisos_acima_aleatorio == 1:
            pisos_abaixo_aleatorio = 2
        elif pisos_acima_aleatorio == 2:
            pisos_abaixo_aleatorio = 1
        else:
            pisos_abaixo_aleatorio = 0
        return pisos_acima_aleatorio, pisos_abaixo_aleatorio


def cota():
    """
    esta função calcula o valor da cota de soleira, como sendo um valor aleatório entre 0 e 2, sendo que pode ser um valor com casas décimais 
    (formatado com 2 casas décimais). 
    """
    cota_aleatoria = "{:.2f}".format(random.uniform(0,2))
    return float(cota_aleatoria)


def altura(n_pisos):
    """
    Esta função determina o valor para a altura da habitação ou edificio em função do número de pisos. 
    A altura é um valor aleatório entre 6 e 10 multiplicado pelo número de pisos. 
    """

    altura = random.uniform(6,10)*n_pisos
    return altura


def area_terreno_construção (tip_aleatoria):
    """
    Esta função calcula o valor da área do terreno em função da tipologia. 
    No caso de a tipologia ser inferior ou igual a 1 então as áreas serão um valor aleatório entre 50 e 120. 
    No caso de a tipologia ser 2 as areas serão um valor aleatório entre 70 e 150. 
    No caso de a tipologia ser 3 as areas serão um valor aleatório entre 90 e 200. 
    No caso de a tipologia ser 4 as areas serão um valor aleatório entre 100 e 250. 
    No caso de a tipologia ser 5 as areas serão um valor aleatório entre 120 e 300. 
    """
    if tip_aleatoria <= 1:
        area_aleatoria = random.randint(50,120)
        area_construcao = random.randint(50,120)
        return area_aleatoria, area_construcao
    elif tip_aleatoria == 2:
        area_aleatoria = random.randint(70, 150)
        area_construcao = random.randint(70, 150)
        return area_aleatoria, area_construcao
    elif tip_aleatoria == 3:
        area_aleatoria = random.randint(90, 200)
        area_construcao = random.randint(90, 200)
        return area_aleatoria, area_construcao
    elif tip_aleatoria == 4:
        area_aleatoria = random.randint(100, 250)
        area_construcao = random.randint(100, 250)
        return area_aleatoria, area_construcao
    elif tip_aleatoria == 5:
        area_aleatoria = random.randint(120, 300) 
        area_construcao = random.randint(120, 300) 
        return area_aleatoria, area_construcao


def areas():
    """
    Esta função calcula os valores da :
    - Área de cedência: valor aleatório entre 0 e 200
    - Área de construção de anexos: valor aleatório entre 50 e 600
    - Área de implantação: valor aleatório entre 100 e 5000
    - Área bruta privativa: valor aleatório entre 100 e 4000
    - Área bruta dependente: valor aleatório entre 100 e 1000
    - Área do Lote: valor aleatório entre 100 e 1000.
    Os outups da função encontram-se nesta mesma ordem.
    """
    area_ced_aleatoria = random.randint(0, 200)  
    area_cons_anexos_aleatoria =  random.randint(50, 600)  
    area_impl_aleatoria =  random.randint(100, 5000) 
    area_bpriv_aleatoria =  random.randint(100, 4000)   
    area_bdep_aleatoria =  random.randint(100, 1000) 
    area_lote_aleatoria=  random.randint(100, 10000)  
    return area_ced_aleatoria, area_cons_anexos_aleatoria, area_impl_aleatoria, area_bpriv_aleatoria, area_bdep_aleatoria, area_lote_aleatoria



def fogos_fracoes():
    """
    Esta função calcula os valores de fogos e das frações, sendo um valor entre 0 e 20
    """
    n_fogos_aleatorios = random.randint(0, 20)  
    n_fracoes_aleatorias = n_fogos_aleatorios
    return n_fogos_aleatorios, n_fracoes_aleatorias



def indices():
    """
    Esta função calcula os índices de impermeabilização, ocupação e utilização, sendo um valor
    aleatório entre 0 e 1, formatando os valores com duas casas décimais. 
    Os outputs são retornados na mesma ordem. 
    """
    ind_impr_aleatorio = "{:.2f}".format(random.random()) 
    ind_ocu_aleatorio =  "{:.2f}".format(random.random()) 
    ind_uti_aleatorio = "{:.2f}".format(random.random()) 
    return ind_impr_aleatorio, ind_ocu_aleatorio, ind_uti_aleatorio



categorias_obra = ["Construção", "Ampliação", "Alteração", "Demolição"]

def categoria_obra(categorias_obra):
    """
    Esta função define a categoria de obra, escolhendo da seguinte lista:

    categorias_obra = ["Construção", "Ampliação", "Alteração", "Demolição"]

    """
    cat_obra_aleatoria = random.choice(categorias_obra)
    return cat_obra_aleatoria



def estimativa (cat_obra_aleatoria, tipologia):
    """
    Esta função calcula a estimativa da obra em função do tipo de obra que é (categoria de obra). 
    No caso de ser contrução o custo é um valor entre 100000 e 1000000. 
    Por outro lado, qualquer outro tipo de categoria, o valor está entre 1000 e 100000. 
    """

    if cat_obra_aleatoria == "Construção":
        if tipologia <= 2:
            estimativa_aleatoria = random.randint(80000, 150000)
            return estimativa_aleatoria
        else:
            estimativa_aleatoria = random.randint(150000, 300000)
            return estimativa_aleatoria 
    else:
        estimativa_aleatoria = random.randint(1000, 100000)
        return estimativa_aleatoria


freguesias_pt = gpd.read_file("../resources/freguesias/Cont_AAD_CAOP2017.shp")
agueda = freguesias_pt[freguesias_pt["Concelho"] == "ÁGUEDA"]


municipios = gpd.read_file("../resources/concelhos/concelhos.shp")
municipio_agueda = municipios[municipios["NAME_2"] == "Águeda"]



mun = municipio_agueda.to_crs("EPSG:3763")
mun

def polygon_random_points (poly, num_points):
    """
    Esta função calcula pontos aleatórios que estão entre os valores máximos e mínimos das coordenadas do municipio de Águeda.
    Recebe como argumentos o polígono e o número de pontos que queremos produzir
    """
    min_x = poly.bounds.minx
    min_y = poly.bounds.miny
    max_x = poly.bounds.maxx
    max_y = poly.bounds.maxy

    points = []
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        points.append(random_point)
    return points

# chama a função criada acima que gera os pontos aleatórios
points = polygon_random_points(mun.geometry, 1000)

#cria um DataFrame com a culuna "geometria" com os pontos criados
pontos = pd.DataFrame(points, columns = ["geometria"])


#cria o geodataframe com os pontos, e após elimina a linha repetida da geometria
gdf = gpd.GeoDataFrame(geometry=pontos.geometria)

#encontrar as freguesias dos pontos gerados
pontos_fichas = gdf.sjoin(agueda, how="left")

pontos_fichas = pontos_fichas.dropna()


r=[]
for i in range(1, len(pontos_fichas)+1):
    r.append(i)

pontos_fichas.insert(0, 'Ficheiro', r)


def coluna_aleatoria():
    """
    Com esta função pretende-se agregar todas as anteriores sobre a criação de dados aleatórios, 
    de forma a criar uma lista com uma linha aleatória, que corresponderia a uma 
    Ficha de Áreas do Município. 
    """
    tipologia = tipo_aleatoria()
    piso = pisos(tipologia)
    fogos = fogos_fracoes()
    categoria = categoria_obra(categorias_obra)

    coluna_aleatoria = ["habitação", tipologia, piso, pisos_local(piso)[0],
        pisos_local(piso)[1] , cota(), altura(piso), area_terreno_construção(tipologia)[0], 
        areas()[0], fogos[0], fogos[1], area_terreno_construção(tipologia)[1], areas()[1],areas()[2],
        areas()[3],areas()[4], estimativa (categoria, tipologia),areas()[5], float(indices()[0]), float(indices()[1]), float(indices()[2]), categoria]
    return coluna_aleatoria


coluna_nova = ["uso_edi", "tip", "n_pisos","n_pisos_ac", "n_pisos_ab", "cota", 
               "altura", "area_terreno", "area_cedencia", "n_fogos", "n_fracoes", 
               "area_total_const", "area_const_anexos", "area_total_imp", "area_bruta_priv", 
               "area_bruta_dep", "estimativa_obra", "area_terreno_lote", 
               "indice_imper", "ind_ocupacao", "ind_utilizacao", "Categoria da Obra"]


x=len(pontos_fichas)

# Ciclo para a produção de 100000 entradas que correspondem a Fichas de Áreas

lista  = []
for i in range(x):
    coluna = coluna_aleatoria()
    lista.append(coluna)

bd_aleatoria = pd.DataFrame(lista, columns = coluna_nova)
if len(pontos_fichas) != len(bd_aleatoria):
    bd_aleatoria = bd_aleatoria[:len(pontos_fichas)]
base_final = pd.concat([bd_aleatoria, pontos_fichas], axis = 1)


base_final.to_excel("../resources/base_dados_aleatoria.xlsx") 