# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import os
os.chdir("C:/Users/Carles/Desktop/DatathonGithub/Sona9-2020/master/src")
# General packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
# My file calls
from config import paths

def RetrievingAllGroups(numpag):
    """
    parameters: numpaginas 
    
    It retrieves from n pages from sona9 all links starting as: 
    "http://www.enderrock.cat/sona9/grup/" (which is the URLtype)        
    """
    URLtype = "http://www.enderrock.cat/sona9/grup/"                    # Url type to save
    AllGrupsLink =[] #OutputList

    for idxnum in range(1,numpag):
        print("evaluating page " +str(idxnum))
        URL = "http://www.enderrock.cat/sona9/grups/pagina"+str(idxnum)  # Url type to retrieve
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser') 
        
        for link in soup.find_all('a', href=True):
            # Evaluating if reference has the type of reference I am looking for
            if URLtype in link['href']:
                # Evaluating if reference already in Outputlist
                if link['href'] not in AllGrupsLink:
                    AllGrupsLink.append(link['href'])

    return AllGrupsLink 

def TakeInfoById(soup, myid):  
    """
    It retrieves info by id using BeautifulSoup
    """
    results = soup.find(id=myid)
    NomdelGroup= results.text.strip()

    return NomdelGroup

def TakeInfoBylabel(soup, labeltext): 
    """
    It retrieves info by label using BeautifulSoup
    """           

    label = soup.find("label", text=labeltext)
    return label.next_sibling.strip()
    

            
def AllInfoInTable(LinksList):
    """
    It takes a list of links and it retrieves:
        Nom del Grup
        Estil
        Població
        Youtube Link
    The output is a pd.Dataframe()    
    """

    NomDelGrup_List =   []
    Estil_List      =   []
    Poblacio_List   =   []
    Canso_list      =   []

    for idx, CurrentURL in enumerate(LinksList):
        print(str(idx+1)+ " out of "+ (str(len(LinksList))))
        page = requests.get(CurrentURL)
        soup = BeautifulSoup(page.content, 'html.parser') 
        
        # Taking NomDelGrup
        NomDelGrup_List.append(TakeInfoById(soup, "nomdelgrup"))
        # Taking Estil
        Estil_List.append(TakeInfoBylabel(soup, "Estil musical"))
        
        # Taking City
        Poblacio_List.append(TakeInfoBylabel(soup, "Ciutat"))
        
        # Taking Video
        for link in soup.find_all('a', href=True):
            if "www.youtube.com" in link['href']:
                Canso_list.append(link['href'])
                break;
        if len(NomDelGrup_List)!=len(Canso_list):
            # Accounting for the fact that can be empty
            Canso_list.append("None")
        
    print("NomDelGrup_List:"+str(len(NomDelGrup_List)))
    print("Estil_List:"+str(len(Estil_List)))    
    print("Poblacio_List:"+str(len(Poblacio_List)))
    print("Canso_list:"+str(len(Canso_list)))    
    TaulaFinal = pd.DataFrame(list(zip(       NomDelGrup_List, 
                                              Estil_List, 
                                              Poblacio_List,
                                              Canso_list)),
                     columns=['NomdelGrup',
                              'Estil', 
                              'Poblacio', 
                              'URLvideoYoutube'])        
    return TaulaFinal

def MainDownload_Sona9(pathtosave, npags = 18):
    # 1. Getting URL per group

    AllLinks = RetrievingAllGroups(npags)
    
    # 2. Put info in tables
    EndTable= AllInfoInTable(AllLinks)
    EndTable.to_csv(pathtosave,encoding='utf-8-sig')
    print("Dataset Created in: "+ pathtosave) 
    return EndTable


def main():    
    ############### Main Paths #########################
    Scrapping_path = paths['Scrap_path']    
    OuputExcel_FileName= "Sona9Grups.csv"
    SavingPath = os.path.join(Scrapping_path,OuputExcel_FileName)
    
    ############### Work Order #########################
    # Executing MainDownload
    
    return MainDownload_Sona9(SavingPath,npags=18)


if __name__ == '__main__':
    main()
