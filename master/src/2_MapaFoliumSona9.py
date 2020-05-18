# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:34:26 2020

@author: Carles
"""


import folium
import pandas as pd
from conf import paths

def main():
    ############### Main Paths #########################
    # Paths
    cwd="C:/Users/Carles/Desktop/DatathonGithub/Sona9-2020/master"
    
    LatLon_path = paths['LatLon_path']    
    Graphic_path = paths['Map_path']
    
    InputExcel_FileName= "Sona9GrupsWithLatLon.csv"    
    OutputMap_htmlName = "Map_Sona9_2020.html"
    
    Reading_path   = cwd+ "/" + LatLon_path      + "/" + InputExcel_FileName
    OutputMap_Path = cwd+ "/" + Graphic_path     + "/" + OutputMap_htmlName
    
    ############### Work Order #########################
    #0. Reading Dataframe 
    df = pd.read_csv(Reading_path)
    #1. Creating a Map using Folium
    map_ = folium.Map(location=[df.iloc[0]['lat'], df.iloc[0]['lon']], 
                      tiles='OpenStreetMap',
                      zoom_start = 6)
    #2. Locate each band on the map by lat lon using and icon of a guitar
    icon_url = "https://img.icons8.com/windows/32/000000/progressive-rock.png"
    for index, row in df.iterrows():
           tooltip = row['NomdelGrup']
           icon = folium.features.CustomIcon(icon_url,icon_size=(28, 30))
           html=""" <h1> """+row['NomdelGrup']+"""</h1><br>
                    Estil: """+ row['Estil'] + """
                    <p>
                    <code>
                        Youtube Video: """+row['URLvideoYoutube']+"""
                    </code>
                    </p>
                    """
           iframe = folium.IFrame(html=html, width=400, height=150)
           popup = folium.Popup(iframe, max_width=1000)
    
           folium.Marker((row['lat'], row['lon']),           
                   popup=popup,
                   tooltip=tooltip,
                   icon=icon).add_to(map_)
    #3. Saving the Result Map in the output path
    map_.save(OutputMap_Path)
    return None


if __name__ == '__main__':
    main()
# =============================================================================
# #Crear el listado de regiones de Italia
# communities_geo = r'italy-provinces.geojson'
# 
# #Representar el mapa choropleth con número de casos por provincia
# choromap_.choropleth(
#     geo_data=communities_geo,
#     data=df_gr,
#     columns=['province', 'total_cases'],
#     key_on='feature.properties.name',
#     fill_color='BuPu', 
#     fill_opacity=1, 
#     line_opacity=1,
#     legend_name='COVID-19 Italy',
#     smooth_factor=0)
# #Visualizar el mapa
# choromap_
# 
# 
# choromap_.save(path_read +"mymap.html")
# =============================================================================
