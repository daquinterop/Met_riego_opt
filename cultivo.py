#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 10:53:14 2019

@author: diego
"""
from datetime import datetime
from datetime import timedelta
import pandas as pd
import os
import pickle
import intercambio_variables
import numpy as np

def Incremento_Produccion(variables):
    #Lectura de variables
    PATH_AC_OUT = variables['PATH_AC_OUT']
    PROJECT_NAME = variables['PROJECT_NAME']
    FeSi = variables['FeSi']
    FeFP = variables['FeFP']
    KtrMean = variables['KtrMean']
    Ktrx = variables['Ktrx']
    Germ = variables['Germ']
    
    #Apertura de archivos de salida de AquaCrop
    CropGrowth = pd.read_table(os.path.join(PATH_AC_OUT, PROJECT_NAME + 
                                            '_CropGrowth.txt'), sep ='\t')
    
    #Pasar las fechas del archivo de salida al formato de fecha
    def FechasDF(DF):
        FechasDF = [datetime(int(DF['Year'][i]), int(DF['Month'][i]), 
                             int(DF['Day'][i])) for i in range(len(DF['Year']))]
        return(FechasDF)
    CropGrowth['Date'] = FechasDF(CropGrowth)
    
    #Rango de fechas de nuestro interés: Siembra - Final del periodo
    DateRange = pd.date_range(FeSi, FeFP)
    
    #Creo vectores con salidas de la simulación para el periodo de interés
    Mask = [i in DateRange for i in CropGrowth['Date']]
    CCref = [CropGrowth['RefCC'][i] for i in range(len(CropGrowth['RefCC'])) 
             if Mask[i]]
    Yield = [CropGrowth['Yield'][i] for i in range(len(CropGrowth['Yield'])) 
             if Mask[i]]
    Bio = [CropGrowth['Bio'][i] for i in range(len(CropGrowth['Bio'])) 
             if Mask[i]]
    Season = [CropGrowth['Season'][i] for i in range(len(CropGrowth['Season'])) 
             if Mask[i]]
        #Verifico si ya es cosecha o no
    Cosecha = bool()
    if Season[-1] == 0:
        Cosecha = True
    else:
        Cosecha = False    
        
    if max(Bio[-7:]) != 0 or Cosecha:
        Germ = True
        
        #Si ya se cosechó al final de la semana, busco el último día de producción
        index = 1
        if Cosecha:
            while Season[-index] == 0:
                index += 1
                
        #Ajuste de CC de acuerdo con Villalobos and Fereres(1990)
        i = CCref[-index - 1]
        CC_adj = 1.72*i-i**2+0.30*i**3
        
        #Calculo del coeficiente de transpiracion del cultivo al final del periodo
        Ktrf = Ktrx*CC_adj
        
        #Coeficiente de Fujimaki y Rendimiento al final del periodo
        Kif = KtrMean/Ktrf
        Yf = Yield[-index]
        Yi = Yield[-7]
        
        #En caso que el día actual sea el día siguiente a la cosecha
        if Yi == 0:
            Yi = Yf
        #Si el día actual es el día de la cosecha YSd = 0
        if index == 7:
            YSd = 0
        else:
            YSd = np.std(Yield[-7:-index])
        
        #Almaceno las variables
        Biof = Bio[-index]
        variables['Cosecha'] = Cosecha
        variables['Biof'] = Biof
        variables['YSd'] = YSd
        variables['Kif'] = Kif
        variables['InYf'] = Yf - Yi 
        variables['Germ'] = Germ
        #Almaceno la fecha tentativa de cosecha
        if Cosecha:
            variables['FeCo'] = DateRange[-index] + timedelta (days = 1)
        intercambio_variables.exp_var(variables)
    else:
        Germ = False
