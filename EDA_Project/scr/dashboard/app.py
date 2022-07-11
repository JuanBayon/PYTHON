import streamlit as st
import os, sys

ruta = __file__
for i in range (3):
    ruta = os.path.dirname(ruta)

sys.path.append(ruta)

from scr.utils.dashboard_tb import Gestor_streamlit

gestor = Gestor_streamlit()

csv_path = ruta + os.sep + 'data' + os.sep +'EDA_analisis.csv'

gestor.configuracion()
df = gestor.cargar_datos(csv_path)


menu = st.sidebar.selectbox('Menu:',
                    options=['home','visualización', 'visualización interactiva', 'filtrado votos', 'obtener datos'])

st.title('Repercusión de las valoraciones de IMDb')

if menu == 'home':
    gestor.menu_home(df)
elif menu == 'visualización':
    gestor.menu_datos()
elif menu == 'visualización interactiva':
    gestor.menu_interactivo(df)
elif menu == 'filtrado votos':
    gestor.menu_filtrado(df)
elif menu== 'obtener datos':
    gestor.menu_obtener_datos()

