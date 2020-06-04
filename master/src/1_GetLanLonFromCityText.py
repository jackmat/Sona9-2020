# -*- coding: utf-8 -*-
"""
Created on Mon May 18 16:26:46 2020

@author: Carles
"""
import os
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from config import paths

def ManualAddings(df):
    df.loc[df.NomdelGrup =="Lluna Plena", 'URLvideoYoutube']= "https://youtu.be/bxksKGbewis"
    df.loc[df.NomdelGrup =="Sabana", 'URLvideoYoutube']= "https://youtu.be/lSzoXbo4VSs"
    df.loc[df.NomdelGrup =="Tomeu Juan Fuster", 'URLvideoYoutube']= "https://www.youtube.com/playlist?list=PLIHZApSkCjI2gbrXGX0sEdxAD38LZ5qPv"
    df.loc[df.NomdelGrup =="Palmira", 'URLvideoYoutube']= "http://youtube.com/watch?v=oG32pvS2PCI"
    df.loc[df.NomdelGrup =="Palmira", 'lat']= 41.2
    df.loc[df.NomdelGrup =="Palmira", 'lon']= 2.2
    df.loc[df.NomdelGrup =="Ideal", 'URLvideoYoutube']= "https://youtu.be/oUs8lQTz5nE"
    df.loc[df.NomdelGrup =="Bona Ventura", 'URLvideoYoutube']= "https://youtu.be/JO_fDelmWfk"
    df.loc[df.NomdelGrup =="Bona Ventura", 'lat']= 39.69
    df.loc[df.NomdelGrup =="Bona Ventura", 'lon']= 2.78
    df.loc[df.NomdelGrup =="Màresan", 'lat']= 40.620200
    df.loc[df.NomdelGrup =="Màresan", 'lon']= 0.592890
    df.loc[df.NomdelGrup =="Estiula", 'lat']= 42.196390
    df.loc[df.NomdelGrup =="Estiula", 'lon']= 2.303340
    df.loc[df.NomdelGrup =="Projecte Castor", 'URLvideoYoutube']= "https://www.youtube.com/watch?v=tzE2cef32OM&list=PLhw6b1QRaV8vlhXBLjhYpRlb_z0dQjgn_"
    

    return df

def PopulationLatLon(Mycities):
    """
    Given a list of Cities, it Outputs its region, latitude and longitude
    """
    lat_list = []
    lon_list = []
    Comunity_list = []
    for idx, city in enumerate(Mycities):
        try:
            print(idx, city)
            address = city.split("(")[0]
            print(address)
            geolocator = Nominatim(user_agent="Your_Name")
            location = geolocator.geocode(address,timeout=10000)
            print(location)
            if location ==None: 
                address = city.split(" ")[0]
                geolocator = Nominatim(user_agent="Your_Name")
                location = geolocator.geocode(address, timeout=10000)

            if  "España" !=(location.address.split(",")[len(location.address.split(","))-1].replace(" ", "")):
                address = city
                geolocator = Nominatim(user_agent="Your_Name")
                location = geolocator.geocode(address, timeout=10000)
                
            Comunity_list.append(location.address.split(",")[len(location.address.split(","))-3])
            lat_list.append(location.latitude)
            lon_list.append(location.longitude)
        except:
            print("Exception occured. Trying again with: ", idx, city)
            address = city.split("(")[0]
            geolocator = Nominatim(user_agent="Your_Name")
            location = geolocator.geocode(address, timeout=10000)
            if location ==None: 
                address = city.split(" ")[0]
                geolocator = Nominatim(user_agent="Your_Name")
                location = geolocator.geocode(address , timeout=10000)
            Comunity_list.append(location.address.split(",")[len(location.address.split(","))-3].replace(" ", ""))
            lat_list.append(location.latitude)
            lon_list.append(location.longitude)
            
    Frame =pd.DataFrame(zip(lat_list, lon_list, Comunity_list), columns =["lat", "lon", "Region"])
    return Frame


def StringTreatment(df):
    """
    It transforms the df.Region manually if certain conditions are met
    """
    df.loc[df.Region ==" Barcelona", 'Region'] = "Catalunya"
    df.loc[df.Region ==" Catalunya", 'Region'] = "Catalunya"
    df.loc[df.Region ==" Lleida", 'Region'] = "Catalunya"
    df.loc[df.Region ==" Girona", 'Region'] = "Catalunya"
    df.loc[df.Region ==" Tarragona", 'Region'] = "Catalunya"
    
    df.loc[df.Region ==" València / Valencia", 'Region'] = "Comunitat Valenciana"
    df.loc[df.Region ==" Alacant / Alicante", 'Region'] = "Comunitat Valenciana"
    df.loc[df.Region ==" Comunitat Valenciana", 'Region'] = "Comunitat Valenciana"
    df.loc[df.Region ==" Castelló / Castellón", 'Region'] = "Comunitat Valenciana"

    df.loc[df.Region =="Palma", 'Region'] = "Illes Balears"
    df.loc[df.Region ==" Illes Balears", 'Region'] = "Illes Balears"
    df.loc[df.Region ==" Menorca", 'Region'] = "Illes Balears"
    df.loc[df.Region ==" Eivissa", 'Region'] = "Illes Balears"
    df.loc[df.Region ==" Pla de Mallorca", 'Region'] = "Illes Balears"
    df.loc[df.Region ==" Llevant", 'Region'] = "Illes Balears"


    return df



def dfTreatment2(df):
    """
    It puts noise to df.lat and df.lon in order for the different bands to appear on the map under different lat lon
    It also creates a variable Nom_Estil as the union of df["NomdelGrup"]+": " +df["Estil"].
    It also creates the variable df.NumRegio according to the region the band is from
    """
    df["Nom_Estil"]=df["NomdelGrup"]+": " +df["Estil"]
    df.loc[df.Region =="Catalunya", 'NumRegio'] = 1
    df.loc[df.Region =="Comunitat Valenciana", 'NumRegio'] = 2
    df.loc[df.Region =="Illes Balears", 'NumRegio'] = 3
    df.loc[df.Region =="AndorralaVella", 'NumRegio'] = 4
    
    df.lat = df.lat + np.random.rand(*df.lat.shape) / 100.0
    df.lon = df.lon + np.random.rand(*df.lon.shape) / 100.0
    
    df["NumRegio"] = df["NumRegio"].astype(str)
    return df


def main ():
    ############### Main Paths #########################
    # Paths
    Scrapping_path = paths['Scrap_path']    
    LatLon_path = paths['LatLon_path']    
    
    InputExcel_FileName= "Sona9Grups.csv"
    OutputExcel_FileName= "Sona9GrupsWithLatLon.csv"    
    
    Reading_path = os.path.join(Scrapping_path,InputExcel_FileName)
    Saving_path  = os.path.join(LatLon_path,OutputExcel_FileName)
    ############### Work Order #########################
    #0. Reading Dataframe    
    df = pd.read_csv(Reading_path,encoding='utf-8-sig')
    # Canvis Manuals
    df.Poblacio.replace({'Vallls (Alt Camp)':'Valls (Alt Camp)'}, inplace = True)
    df.Poblacio.replace({'Barcelona (Alt Penedès)':'Vilafranca del Penedès (Alt Penedès)'}, inplace = True)

    #1. Reading Poblacio column
    Mycities = df.Poblacio

    #2. Getting lat & lon
    Frame = PopulationLatLon(Mycities)
    #3. Merging it with current data.frame()

    AllTogether = pd.concat([df.reset_index(drop=True), Frame], axis=1)
    df2 = AllTogether.copy()
    #4. Dataset Treatment
    df3 = StringTreatment(df2)
    df4 = dfTreatment2(df3)
    
    #Manual Changes
    df5 = ManualAddings(df4)
    # Output
    df5.to_csv(Saving_path, encoding='utf-8-sig')

if __name__ == '__main__':
    main()
    
  