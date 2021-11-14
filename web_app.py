import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import folium

st.title('Streamlit Dashboard')
st.sidebar.title('Sidebar')

option = st.sidebar.selectbox('Select Data Files', ('2016_data', '2017_data', '2018_data', '2019_data', '2020_data'))
option_radio = st.sidebar.radio('Select Any Values:', ['Appartement', 'Dépendance', 'Local industriel. commercial ou assimilé', 'Maison'])  

# Loading Data
@st.cache(allow_output_mutation=True)
def load_data(filepath):
    df = pd.DataFrame()
    specific_cols = [
        'id_mutation', 'date_mutation', 'numero_disposition', 'nature_mutation',
        'valeur_fonciere', 'adresse_numero', 'adresse_nom_voie', 'adresse_code_voie',
        'code_postal', 'code_commune', 'nom_commune', 'code_departement', 
        'id_parcelle', 'type_local', 'surface_reelle_bati', 'nombre_pieces_principales',
        'code_nature_culture', 'nature_culture', 'surface_terrain',
        'longitude', 'latitude'
    ]
    temp = pd.read_csv(filepath, iterator=True, chunksize=300000, low_memory=False, usecols=specific_cols)
    df = pd.concat(temp, ignore_index=True)
    return df

# Function for bar plot
def bar_plot(data):
    fig = px.bar(
        x = data['nature_culture'].value_counts().index,
        y = data['nature_culture'].value_counts().values,
        title = 'Bar Plot for Nature Culture',
        text = data['nature_culture'].value_counts().values
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    fig.update_layout(
        uniformtext_mode='hide',
        width= 600, 
        height= 400,
        hovermode = 'x'
    )
    return fig

# Function for Slider plot
def slider_plot(data):
    # Dataframe
    data['date_mutation'] = pd.to_datetime(data['date_mutation'])
    df = data.groupby(['date_mutation']).size().reset_index(name='counts')
    
    fig = px.line(
        x = df['date_mutation'],
        y = df['counts'],
        title = 'Count of Transfers conducted per day'
    )
    fig.update_layout(
        hovermode = 'x',
        xaxis = dict(
            rangeselector = dict(
                buttons = list([
                    dict(
                        count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(
                        count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"
                    ),
                    dict(step="all")
                ])
            ),
            rangeslider = dict(
                visible=True
            ),
        ),
        width= 600, 
        height= 400
    )
    return fig

# Histogram Plot function
def histogram(data):
    prices = sorted(data)

    fig = px.histogram(x=prices, nbins=20)
    fig.update_layout(
        hovermode = 'x',
        title = 'Distribution of Valeur_fonciere data',
        width= 600, 
        height= 300
    )
    return fig

# Pie Chart Plot Function
def pie(data):
    fig = px.pie(
        values = data.value_counts().index, 
        names = data.value_counts().values,
        hole = .4
    )
    fig.update_traces(
        textposition='inside'
    )
    fig.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        title = 'Pie Chart for code_commune types',
        width= 600, 
        height= 400
    )
    return fig

# Scatter plot function for
def scatter_plot(data):
    scatter_plt = data
    df = scatter_plt.groupby(['adresse_nom_voie', 'nature_mutation']).size().reset_index(name='counts')

    fig = px.scatter(
        df,
        x = 'adresse_nom_voie',
        y = 'counts',
        color = 'counts'
    )
    fig.update_layout(
        hovermode = 'x',
        title = 'Scatter plot between adresse_nom_voie and total counts',
        width= 600, 
        height= 400
    )
    return fig


# Main Function
if __name__ == "__main__":
    # '2016_data', '2017_data', '2018_data', '2019_data', '2020_data'
    
    # Setting up column for plots
    plot_1, plot_2 = st.columns(2)
    
    # Select Files
    if option == '2016_data':
        data = load_data('./dataset/full_2016.csv')
        # Streamlit charts variables
        type_local = pd.DataFrame(data['type_local'].value_counts())
        
        # Select box
        if option_radio == 'Appartement':
            df = data[data['type_local'] == 'Appartement']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
        elif option_radio == 'Dépendance':    
            df = data[data['type_local'] == 'Dépendance']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(data['code_commune']))
            plot_1.plotly_chart(bar_plot(data))
            plot_2.plotly_chart(histogram(data['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(data[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(data))
        
        elif option_radio == 'Local industriel. commercial ou assimilé':    
            df = data[data['type_local'] == 'Local industriel. commercial ou assimilé']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
            
        elif option_radio == 'Maison': 
            df = data[data['type_local'] == 'Maison']   
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
    
    if option == '2017_data':
        data = load_data('./dataset/full_2017.csv')
        # Streamlit charts variables
        type_local = pd.DataFrame(data['type_local'].value_counts())
        
        # Select box
        if option_radio == 'Appartement':
            df = data[data['type_local'] == 'Appartement']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
        elif option_radio == 'Dépendance':    
            df = data[data['type_local'] == 'Dépendance']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(data['code_commune']))
            plot_1.plotly_chart(bar_plot(data))
            plot_2.plotly_chart(histogram(data['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(data[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(data))
        
        elif option_radio == 'Local industriel. commercial ou assimilé':    
            df = data[data['type_local'] == 'Local industriel. commercial ou assimilé']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
            
        elif option_radio == 'Maison': 
            df = data[data['type_local'] == 'Maison']   
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
    
    if option == '2018_data':
        data = load_data('./dataset/full_2018.csv')
        # Streamlit charts variables
        type_local = pd.DataFrame(data['type_local'].value_counts())
        
        # Select box
        if option_radio == 'Appartement':
            df = data[data['type_local'] == 'Appartement']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
        elif option_radio == 'Dépendance':    
            df = data[data['type_local'] == 'Dépendance']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(data['code_commune']))
            plot_1.plotly_chart(bar_plot(data))
            plot_2.plotly_chart(histogram(data['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(data[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(data))
        
        elif option_radio == 'Local industriel. commercial ou assimilé':    
            df = data[data['type_local'] == 'Local industriel. commercial ou assimilé']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
            
        elif option_radio == 'Maison': 
            df = data[data['type_local'] == 'Maison']   
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
    if option == '2019_data':
        data = load_data('./dataset/full_2019.csv')
        # Streamlit charts variables
        type_local = pd.DataFrame(data['type_local'].value_counts())
        
        # Select box
        if option_radio == 'Appartement':
            df = data[data['type_local'] == 'Appartement']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
        elif option_radio == 'Dépendance':    
            df = data[data['type_local'] == 'Dépendance']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(data['code_commune']))
            plot_1.plotly_chart(bar_plot(data))
            plot_2.plotly_chart(histogram(data['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(data[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(data))
        
        elif option_radio == 'Local industriel. commercial ou assimilé':    
            df = data[data['type_local'] == 'Local industriel. commercial ou assimilé']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
            
        elif option_radio == 'Maison': 
            df = data[data['type_local'] == 'Maison']   
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
    if option == '2020_data':
        data = load_data('./dataset/full_2020.csv')
        # Streamlit charts variables
        type_local = pd.DataFrame(data['type_local'].value_counts())
        
        # Select box
        if option_radio == 'Appartement':
            df = data[data['type_local'] == 'Appartement']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
        
        elif option_radio == 'Dépendance':    
            df = data[data['type_local'] == 'Dépendance']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(data['code_commune']))
            plot_1.plotly_chart(bar_plot(data))
            plot_2.plotly_chart(histogram(data['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(data[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(data))
        
        elif option_radio == 'Local industriel. commercial ou assimilé':    
            df = data[data['type_local'] == 'Local industriel. commercial ou assimilé']
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))
            
        elif option_radio == 'Maison': 
            df = data[data['type_local'] == 'Maison']   
            # Streamlit plots
            # st.map(map_data)
            plot_1.bar_chart(type_local)
            # Plotly charts
            plot_2.plotly_chart(pie(df['code_commune']))
            plot_1.plotly_chart(bar_plot(df))
            plot_2.plotly_chart(histogram(df['valeur_fonciere']))
            plot_1.plotly_chart(scatter_plot(df[['adresse_nom_voie', 'valeur_fonciere', 'nature_mutation', 'date_mutation']]))
            plot_2.plotly_chart(slider_plot(df))

            #latitude = pd.to_numeric(data['latitude'], errors='coerce').astype('float32')
            #longitude = pd.to_numeric(data['longitude'], errors='coerce').astype('float32')
            
            latitude = df['latitude'].apply(np.float64)
            longitude = df['longitude'].apply(np.float64)
            map_data = {
                'longitude': longitude,
                'latitude': latitude
            }
            map_data = pd.DataFrame(map_data)
            fig = px.scatter_geo(
                lat = map_data['latitude'],
                lon = map_data['longitude'],
                # hover_name="name"
            )
            st.plotly_chart(fig)
            
            #st.write(type(latitude[0]))
            #st.table(map_data.head(5))
            #st.map(map_data)
            #import numpy as np
            #df_2 = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
            #st.map(df_2)

            latitude = pd.to_numeric(df['latitude'], errors='coerce').astype('float32')
            longitude = pd.to_numeric(df['longitude'], errors='coerce').astype('float32')
            map_data = {
                'longitude': longitude,
                'latitude': latitude
            }
            map_data = pd.DataFrame(map_data)
            map_data['combine'] = list(zip(map_data.latitude, map_data.longitude))
            # for i in map_data['combine']:
            #     print(1)
            #     if len(i) != 2:
            #         print(type(i), len(i))

            st.table(map_data['combine'])
            
            map = folium.Map(location=map_data['combine'], zoom_start=14, control_scale=True)
            folium_static(map)