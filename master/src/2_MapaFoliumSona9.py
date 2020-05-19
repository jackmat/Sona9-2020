# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:34:26 2020

@author: Carles
"""
import sys
sys.path.insert(0,'folium')

import folium
import folium.plugins
import folium
import pandas as pd
#from conf import paths
from folium.features import *



import os
os.chdir("C:/Users/Carles/Desktop/DatathonGithub/Sona9-2020/master")
         
class DivIcon(MacroElement):
    def __init__(self, html='', size=(30,30), anchor=(0,0), style=''):
        """TODO : docstring here"""
        super(DivIcon, self).__init__()
        self._name = 'DivIcon'
        self.size = size
        self.anchor = anchor
        self.html = html
        self.style = style
        self._template = Template(u"""
            {% macro header(this, kwargs) %}
              <style>
                .{{this.get_name()}} {
                    {{this.style}}
                    }
              </style>
            {% endmacro %}
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.divIcon({
                    className: '{{this.get_name()}}',
                    iconSize: [{{ this.size[0] }},{{ this.size[1] }}],
                    iconAnchor: [{{ this.anchor[0] }},{{ this.anchor[1] }}],
                    html : "{{this.html}}",
                    });
                {{this._parent.get_name()}}.setIcon({{this.get_name()}});
            {% endmacro %}
            """)


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
           html="<h1> "+row['NomdelGrup']+"</h1><br> Estil: "+ row['Estil'] + \
                    "<p><code>Youtube Video: <a href="+\
                    row['URLvideoYoutube']+"target='_blank'>"+\
                    row['URLvideoYoutube']+"</a>"+\
                    "</code></p>"
                    
           iframe = folium.IFrame(html=html, width=400, height=150)
           popup = folium.Popup(iframe, max_width=1000)
    
           folium.Marker((row['lat'], row['lon']),           
                   popup=popup,
                   tooltip=tooltip,
                   icon=icon).add_to(map_),
           folium.Marker(
                    (row['lat']-0.0001, row['lon']),
                    icon=DivIcon(
                    size=(25,20),
                    anchor=(25,0),
                    html= "<b>"+ row['NomdelGrup'] +"</b>",
                    style="""
                        font-size:12px;
                        color:black;
                        background-color: transparent;
                        border-color: transparent;
                        text-align: right;
                        """
                )).add_to(map_)
           
           legend_html = """
                         <div style="position: fixed; 
                         bottom: 50px; right: 50px; width: 100px; height: 60px; 
                         border:2px solid grey; z-index:9999; font-size:14px;
                         background-color:white;
                         ">&nbsp; <b>Llegenda</b> <br>
                         &nbsp; Grup &nbsp; <img src="https://img.icons8.com/windows/32/000000/progressive-rock.png"><br>
                          </div>
                         """
           map_.get_root().html.add_child(folium.Element(legend_html))
           
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
