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
    
    df.loc[df.Region =="Palma", 'Region'] = "Illes Balears"
    df.loc[df.Region ==" Illes Balears", 'Region'] = "Illes Balears"
    return df



def dfTreatment2(df):
    """
    It puts noise to df.lat and df.lon in order for the different bands to appear on the map under different lat lon
    It also creates a variable Nom_Estil as the union of df["NomdelGrup"]+": " +df["Estil"].
    It also creates the variable df.NumRegio according to the region the band is from
    """
    df["Nom_Estil"]=df["NomdelGrup"]+": " +df["Estil"]
    df["NumRegio"]=0
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

    # Output
    df4.to_csv(Saving_path, encoding='utf-8-sig')

if __name__ == '__main__':
    main()