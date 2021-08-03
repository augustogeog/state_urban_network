#region IMPORTING PACKAGES
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import plotly.io as pio
import app_functions as app
pd.options.display.float_format = "{:,.2f}".format
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
import pickle
#endregion importing packages

#region SIDEBAR
df_territory = app.load_df_territory()
#uf = st.sidebar.selectbox(label='UF', options=df_territory.uf.unique())
uf = 'BA'
#options = app.filter_municipalities_by_uf(uf=uf, df=df_territory)
dict_pop_cluster = {
    'Salvador':2930709
    ,'Brejões - Nova Itarana':2904308
    ,'Cachoeira - Muritiba - Governador Mangabeira':2929008
    ,'Conceição do Almeida - Sapeaçu':2929602
    ,'Santa Maria da Vitória':2929057
    ,'Ubaitaba - Aurelino Leal':2932200
    ,'Vera Cruz - Itaparica':2933208
}

st.header(list(dict_pop_cluster.values()))

pop_cluster = st.sidebar.selectbox(label='Arranjo Populacional', options=list(dict_pop_cluster.keys()))
cod_municipio = dict_pop_cluster[pop_cluster]
#cod_municipio = app.get_cod_municipio(df=df_territory, uf=uf, municipio=municipio)
municipio_name = app.load_mun_name(cod_municipio=cod_municipio)
#endregion SIDEBAR

st.markdown(type(cod_municipio))





#region HEADER
st.markdown(f"<h1 style='text-align: right; color: black;'>Rede Urbana do Estado da Bahia</h1>", unsafe_allow_html=True)
st.markdown(f'## {pop_cluster}')
#endregion HEADER

#region COMMUTING DATA
import streamlit.components.v1 as components
df = pd.read_csv('data/pop/arranjos populacionais/tab01.csv', sep=';', decimal=',', thousands='.')
if cod_municipio in df['Código do município'].unique():
#    fig_arranjo = app.plot_arranjo(cod_municipio=cod_municipio)
#    st.plotly_chart(fig_arranjo, use_container_width=True)

    st.markdown(f"<p style='text-align: left; color: black; font-size:18px'><b>Mobilidade Pendular do Arranjo Populacional<b></p>", unsafe_allow_html=True)
    kepler_map = app.plot_commuting(cod_municipio=cod_municipio)
    htm = kepler_map._repr_html_()
    components.html(htm, height=600)
#endregion COMMUTING DATA