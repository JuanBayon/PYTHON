import streamlit as st
from PIL import Image
import pandas as pd
import os, sys

ruta = os.path.abspath(__file__)
for i in range(3):
    ruta = os.path.dirname(ruta)

sys.path.append(ruta)

from scr.utils.calculadora_estadistica import Calculadora_estadistica


class Gestor_streamlit:

    def configuracion(self):
        st.set_page_config(page_title='Repercusión de las valoraciones de IMDb', page_icon=':electric_plug:', layout="wide")


    def menu_home(self, df):
        img = Image.open(ruta + os.sep + 'resources' + os.sep + 'dataset-cover.png')
        st.image(img, use_column_width='auto')
        
        with st.beta_expander("AFECTAN LAS VALORACIONES DE IMDb A LA RECAUDACIÓN EN TAQUILLA?"):
            st.write("""
            Las páginas de cine tienen muchos usuarios y sus
            valoraciones sirven de referencia. Sin embargo, 
            es esto cierto? Aquí presesnto unos datos para poder
            comprobarlo!""")

        st.write("""Como hipotesis principal se comprobara si las valoraciones que se 
                    hacen de las peliculas en IMDb estan directamente relacionadas con la recaudacion de las mismas.
                    Ademas se plantean antes varias posibilidades de estudio segmentadas que permitiran comprobar 
                    que no se generalizan las conclusiones, estudiando las votaciones por sexo, edad o procedencia. 
                    Se comprobaran ademas otras variables como el pais de procedencia o el genero para asegurar 
                    que la muestra es lo suficientemente variada""")
        
        st.write("Estos son los datos de partida")
        st.dataframe(df)
    

    @st.cache(suppress_st_warning=True)
    def cargar_datos(self, csv_path):
        df = pd.read_csv(csv_path)
        return df


    def menu_datos(self):

        st.subheader('Distribución de películas por géneros')
        img_generos = Image.open(ruta + os.sep + 'reports' + os.sep + 'distribucion_generos.png')
        st.image(img_generos, use_column_width='auto')
        st.write('Thriller, comedia o acción son los siguientes. Es una muestra variada, que representa todo tipo de géneros, 23 en total.')


        st.subheader('Distribución de películas por país de creación')
        img_generos = Image.open(ruta + os.sep + 'reports' + os.sep + 'importancia_paises.png')
        st.image(img_generos, use_column_width='auto')
        st.write("""Estados unidos es la procedencia predominante en la muestra. 
                    Son 58 países en total. Reino Unido es la segunda y luego el resto 
                    de valores tienen mucha menos representación. el idioma de casi 
                    todos los títulos es el inglés""")

        st.subheader('Distribución de películas por año')
        img_generos = Image.open(ruta + os.sep + 'reports' + os.sep + 'distribucion_generos.png')
        st.image(img_generos, use_column_width='auto')
        st.write("""de la muestra se retiran todo las entradas anteriores a 1190. 
                    En el año 1990 se creó la página web IMDb por lo que las películas 
                    anteriores no sirven para el estudio porque sus valoraciones 
                    no pudieron afectar a la recaudación""")


        st.subheader("La muestra es variada, refleja todo tipo de películas en cuanto a género, país de procedencia o año de creación. En cuanto a los actores o director es variada y además no repercuten en la distribución de votos.")


        st.subheader('Distribución de los votos por edades y sexo')
        img_generos = Image.open(ruta + os.sep + 'reports' + os.sep + 'valoraciones_edad_genero.png')
        st.image(img_generos, use_column_width='auto')
        st.write("""Tanto por tramos de edad como por sexo las votaciones se mantienen 
                    con una distribución constante. La media es prácticamente constante 
                    para el grupo que elijamos""")


        st.subheader('Distribución de los votos en EEUU y en el resto')
        img_generos = Image.open(ruta + os.sep + 'reports' + os.sep + 'distribucion_procedencia.png')
        st.image(img_generos, use_column_width='auto')
        st.write("""El comportamiento de los usuarios de eeuu está alineado con el del resto del mundo. 
                    Se comprueba que la distribución es igual y está totalmente relacionada. 
                    Las valoraciones son iguales en los dos grupos""")

        st.subheader("""
                        En resumen ni la edad, ni el sexo ni la procedencia afectan a las valoraciones. Todos los grupos votan igual.""")


        st.subheader('Relación de los votos con la recudación')
        img_generos = Image.open(ruta + os.sep + 'reports' + os.sep + 'correlacion_conclusiones.png')
        st.image(img_generos, use_column_width='auto')
        st.write("""Las mayores relaciones son entre conceptos similares. Las valoraciones no afectan a la recaudación, 
                    pero el presupuesto y la cantidad de votos sí""")


        st.header('Conclusiones')

        st.subheader('la respuesta a la hipótesis inicial')
        st.write("""Las valoraciones de IMDb no afectan a las recaudaciones""")

        st.subheader('además hemos conseguido saber')
        st.write("""
                El presupuesto afecta a las recaudaciones directamente. La publicidad detrás de ese presupuesto será posiblemente la razón.
                Las votaciones se reparten igual independientemente del sexo, edad o procedencia.
                La cantidad de votos afecta a las recaudaciones, aunque no de manera tan determinante como el presupuesto.""")


    def menu_interactivo(self, df):

        calculadora_estadistica = Calculadora_estadistica(df)
        df_pais = calculadora_estadistica.agrupado_ganancias('country', dummie=True, valoracion=True)
        df_genero = calculadora_estadistica.agrupado_ganancias('genres', dummie=True, valoracion=True)

        st.subheader('Distribución de votos por país')
        votos = df_pais[['imdb_mean_vote']].sort_values('imdb_mean_vote', ascending=False)
        st.bar_chart(votos)

        st.subheader('Distribución de votos por género de película')
        votos1 = df_genero[['imdb_mean_vote']].sort_values('imdb_mean_vote', ascending=False)
        st.bar_chart(votos1)

        st.subheader('Distribución de recaudación por género de película')
        recaudacion1 = df_genero[['worlwide_gross_income']].sort_values('worlwide_gross_income', ascending=False)
        st.bar_chart(recaudacion1)


    def menu_obtener_datos(self):
        st.subheader('DESCARGA DE DATOS EN FORMATO JSON')
        st.write('Tienes a tu disposición los datos de este estudio para tu propio uso.')
        if st.button('Descargar'):
            download = pd.read_json('http://localhost:8008/get_data?eltoken=Q76903092')
            st.write('Tus datos se han descargado')
            st.dataframe(download)


    def menu_filtrado(self, df):

        st.sidebar.subheader('CONOCE LOS DATOS')
        st.sidebar.subheader('Elige los filtros que quieres aplicar')
        filtro_mujer, filtro_hombre, edad, filtro_edad, filtro_hombre_mujer = self.opciones_filtros()

        st.subheader('SE MUESTRA PRIMERO UNA REPRESENTACIÓN DE LOS USUARIOS AGRUPADOS')
        st.subheader('Muestra de votos conjunta de los usuarios de Imdb')
        imdb_ratings = df['imdb_ratings'].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
        st.bar_chart(imdb_ratings)
        
        df1, df2, df3 = self.filtrar(df, filtro_mujer, filtro_hombre, edad, filtro_edad, filtro_hombre_mujer)

        self.graficas(imdb_ratings, df1, df2, df3, filtro_mujer, filtro_hombre, edad, filtro_edad, filtro_hombre_mujer)


    def opciones_filtros(self):
        filtro_mujer = st.sidebar.checkbox('Quiero mostrar las mujeres')
        filtro_hombre = st.sidebar.checkbox('Quiero mostrar los hombres')
        filtro_hombre_mujer = st.sidebar.checkbox('Quiero mostrar ambos')

        edad = st.sidebar.selectbox(
            'Selecciona la edad que te interese:',
            options = ['De 0 a 18', 'De 18 a 30', 'De 30 a 45', 'Más de 45'])
        filtro_edad = st.sidebar.checkbox('Quiero filtrar por edad')

        return filtro_mujer, filtro_hombre, edad, filtro_edad, filtro_hombre_mujer
    

    def filtrar(self, df, filtro_mujer, filtro_hombre, edad, filtro_edad, filtro_hombre_mujer):

        df1 = None
        df2 = None
        df3 = None

        if filtro_hombre_mujer or filtro_mujer or filtro_hombre:
            if filtro_hombre_mujer:
                if filtro_edad and edad == 'De 0 a 18':
                    df1 = df.iloc[:, 15].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'De 18 a 30':
                    df1 = df.iloc[:, 16].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'De 30 a 45':
                    df1 = df.iloc[:, 17].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'Más de 45':
                    df1 = df.iloc[:, 18].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                else:
                    df1 = df.iloc[:, 14].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')

            if filtro_mujer:
                if filtro_edad and edad == 'De 0 a 18':
                    df2 = df.iloc[:, 25].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'De 18 a 30':
                    df2 = df.iloc[:, 26].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'De 30 a 45':
                    df2 = df.iloc[:, 27].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'Más de 45':
                    df2 = df.iloc[:, 28].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                else:
                    df2 = df.iloc[:, 24].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')

            if filtro_hombre:
                if filtro_edad and edad == 'De 0 a 18':
                    df3 = df.iloc[:, 20].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'De 18 a 30':
                    df3 = df.iloc[:, 21].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'De 30 a 45':
                    df3 = df.iloc[:, 22].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                elif filtro_edad and edad == 'Más de 45':
                    df3 = df.iloc[:, 23].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
                else:
                    df3 = df.iloc[:, 19].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')

        return df1, df2, df3


    def graficas(self, df, df1, df2, df3, filtro_mujer, filtro_hombre, edad, filtro_edad, filtro_hombre_mujer):

        st.subheader('SE MUESTRAN AHORA LOS DATOS FILTRADOS PARA SU COMPARACIÓN')
    
        if filtro_mujer:
            if filtro_edad:
                st.subheader(f'Datos filtrados. Mujeres. {edad}')
                st.bar_chart(df2)  
            else:
                st.subheader('Datos filtrados. Mujeres')
                st.bar_chart(df2) 
        else:
            st.subheader('Datos sin filtrar')
            imdb_ratings = df['imdb_ratings'].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
            st.bar_chart(imdb_ratings)
            
        if filtro_hombre:
            if filtro_edad:
                st.subheader(f'Datos filtrados. Hombres. {edad}')
                st.bar_chart(df1)  
            else:
                st.subheader('Datos filtrados. Hombres')
                st.bar_chart(df1)  
        else: 
            st.subheader('Datos sin filtrar')
            imdb_ratings = df['imdb_ratings'].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
            st.bar_chart(imdb_ratings)

        if filtro_hombre_mujer:
            if filtro_edad:
                st.subheader(f'Datos filtrados ambos sexos. {edad}')
                st.bar_chart(df3)  
            else:
                st.subheader('Datos sin filtrar')
                st.bar_chart(df3)
        else:
            st.subheader('Datos sin filtrar')
            imdb_ratings = df['imdb_ratings'].value_counts().reset_index().sort_values('index', ascending=False).set_index('index')
            st.bar_chart(imdb_ratings)

