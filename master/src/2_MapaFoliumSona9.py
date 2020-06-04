# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:34:26 2020

@author: Carles
"""


import os
os.chdir("C:/Users/Carles/Desktop/DatathonGithub/Sona9-2020/master/src")
import sys
sys.path.insert(0,'folium')
#pyproj_datadir="C:/Users/Carles/Anaconda3/Library/share"

# =============================================================================
# import pyproj
# pyproj.Proj("+init=epsg:4326")
# 
# =============================================================================
import folium
import folium.plugins
import folium
import pandas as pd
from config import paths
from folium.plugins import MarkerCluster
from folium.plugins import Search
from shapely.geometry import Point
from geopandas import GeoDataFrame
from jinja2 import Template
from branca.element import (Element, Figure, JavascriptLink, MacroElement)
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
   
    LatLon_path = paths['LatLon_path']    
    Graphic_path = paths['Map_path']
    
    InputExcel_FileName= "Sona9GrupsWithLatLon.csv"    
    OutputMap_htmlName = "Map_Sona9_2020.html"
    
    Reading_path   = os.path.join(LatLon_path, InputExcel_FileName)
    OutputMap_Path = os.path.join(Graphic_path, OutputMap_htmlName)
    
    ############### Work Order #########################
    #0. Reading Dataframe 
    df = pd.read_csv(Reading_path, encoding='utf-8-sig')
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]

    crs = {'init': 'epsg:4326'}
    gdf = GeoDataFrame(df.drop(['lon', 'lat'], axis=1), crs=crs, geometry=geometry)
    #1. Creating a Map using Folium
    map_ = folium.Map(location=[df.iloc[0]['lat'], df.iloc[0]['lon']], 
                      tiles='OpenStreetMap',
                      zoom_start = 6)
    #2. Locate each band on the map by lat lon using and icon of a guitar
    icon_url = "https://img.icons8.com/windows/32/000000/progressive-rock.png"
    marker_cluster = MarkerCluster().add_to(map_)
    marker_cluster2 = MarkerCluster().add_to(map_)
    for index, row in df.iterrows():
           
           tooltip = row['NomdelGrup']
           icon = folium.features.CustomIcon(icon_url,icon_size=(28, 30))
           html="<h1> "+row['NomdelGrup']+"</h1><br> Estil: "+ row['Estil'] + \
                    "<p><code>Youtube Video: <a href='"+\
                    row['URLvideoYoutube']+"' target='_blank'>"+\
                    row['URLvideoYoutube']+"</a>"+\
                    "</code></p>"
                          
                    
           iframe = folium.IFrame(html=html, width=400, height=150)
           popup = folium.Popup(iframe, max_width=1000)



           folium.Marker((row['lat'], row['lon']),           
                   popup=popup,
                   tooltip=tooltip,
                   icon=icon).add_to(marker_cluster),
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
                )).add_to(marker_cluster2)
           
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

    style_function = lambda x: {
                                'color': 'black',
                                'weight':2,
                                'fillOpacity':0.5
                                }

    NomdelGrup_check = folium.GeoJson(gdf,
                        name="NomdelGrup",
                        style_function=style_function,
                        tooltip=folium.GeoJsonTooltip(
                            fields=['NomdelGrup'],
                            aliases=['NomdelGrup'], 
                            localize=True
                        )
                    ).add_to(map_)
                        
    Search(
                        layer=NomdelGrup_check,
                        geom_type='Point',
                        placeholder='Busca el teu Grup de Música',
                        collapsed=False,
                        
                        search_label='NomdelGrup'
                        ).add_to(map_)
    folium.LayerControl().add_to(map_)                       
    #3. Saving the Result Map in the output path
    map_.save(OutputMap_Path)
    
    return None


if __name__ == '__main__':
    main()
