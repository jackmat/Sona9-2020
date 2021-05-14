# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 19:58:51 2021

@author: Carles
"""

import pandas as pd
import os
from config import paths



def main():  
    """
    Join Different table years and add year
    """    
    LatLon_path = paths['LatLon_path'] 
    AllData_path  = paths['AllData']    
    OutputExcel_FileName= "FinalDatasetSona9GrupsWithLatLon.csv"    
    Saving_path  = os.path.join(AllData_path,OutputExcel_FileName)
    
    myfiles = os.listdir(LatLon_path)
    for file in myfiles:
        print(file)
        df = pd.read_csv(LatLon_path +"/"+file, encoding='utf-8-sig')
        print(file[0:4])
        df["yearDownload"]= file[0:4]
        if file[0:4] =="2020":
            Outputdf = df.copy()
           
        else:
            Outputdf = pd.concat([Outputdf, df]).reset_index(drop=True) 
    
    
    Outputdf.to_csv(Saving_path, encoding='utf-8-sig')

if __name__ == '__main__':
    main()
