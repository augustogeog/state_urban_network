import geopandas as gpd
import pandas as pd
import plotly.express as px
import json
import numpy as np
import plotly.io as pio
pio.renderers.default = 'plotly_mimetype+notebook'
import os
from urllib import request
import geodata as geo
from zipfile import ZipFile
import app_functions as app
import plotly.graph_objects as go


def load_sector_geodataframe(uf,cod_municipio):
    cod_municipio = str(cod_municipio)
    gdf = gpd.read_file(f'data/territorio/setores2010/{uf}/{cod_municipio}/{cod_municipio}.shp')
    return gdf

def plot_density_map(gdf):

#    gdf.drop(labels=['CD_GEOCODM', 'NM_MUNICIP', 'CD_GEOCODB'], axis=1, inplace=True)
    gdf['Pop/ha'] = gdf['Pop/ha'].fillna(0).astype(np.int64)
    gdf['Hab/ha'] = pd.cut(gdf['Pop/ha'], bins=[0, 10,25,50,75,100,9999999], labels=['Até 10', '10 a 25', '25 a 50', '50 a 75', '75 a 100', 'acima de 100'])
    gdf['Hab/ha'].fillna('Até 10', inplace=True)

    
    lon = gdf.dissolve(by='NM_MUNICIP').centroid.x[0]
    lat = gdf.dissolve(by='NM_MUNICIP').centroid.y[0]

    minx, miny, maxx, maxy = gdf.total_bounds
    max_bound = max(abs(maxx-minx), abs(maxy-miny)) * 111
    zoom = 12.7 - np.log(max_bound)

    fig_map = px.choropleth_mapbox(
        data_frame=gdf
        , geojson=gdf.geometry
    #    , featureidkey=gdf.index
        , locations=gdf.index
        , color='Hab/ha'
    #    , hover_name='CD_GEOCODI'
        , hover_data=None
        , zoom=zoom
        ,center={"lat": lat, "lon": lon}
        , mapbox_style="carto-positron"
        , title='<b>Densidade Demográfica<b>'
        , template=None
        , width=None
        , height=400
        , opacity=0.3
        , category_orders={'Hab/ha':['Até 10', '10 a 25', '25 a 50', '50 a 75', '75 a 100', 'acima de 100']}
        , color_discrete_sequence=px.colors.sequential.RdBu_r[5:]
        )
    
    fig_map.update_layout(margin=dict(l=0, r=0, b=40, t=40))
    fig_map.layout.title.font.size = 18
    fig_map.update_traces(marker_line_width=0.1)

    return fig_map

cod_municipio = 3550308

gdf = load_sector_geodataframe(uf='SP', cod_municipio=3550308)

fig = plot_density_map(gdf=gdf); 

fig.to_json(f'TESTEJSONSAMPA.json')