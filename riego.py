#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 14:37:31 2019

@author: diego
"""
import os
os.chdir('/home/meteo1a/Documentos/Diego/Scripts/Metodologia')
#import conversion
from datetime import datetime
import intercambio_variables
import pickle

#Inicializo variables
def Costo_Riego(variables):
    Q = variables['Q']
    Ln = variables['Ln']
    Ef = variables['Ef']
    PE = variables['PE']
    RC = variables['RC']
    VUE = variables['VUE']
    PA = variables['PA']
    PW = variables['PW']
    FM = variables['FM']
    CP = variables['CP']
    PM = variables['PM']
#    FeAc = variables['FeAc']
#    FISR = variables['FISR']
#    I = variables['I']
    
    for i in variables.keys():
        vars()[i]=variables[i]
    
    def tiempo_total(Q, L):
        return (10000.0 * L/1000 / Q)
    
    #Lamina Bruta
    Lb = Ln/Ef
    
    #Tiempo de vida del sistema de riego
#    n = FeAc - FISR
#    n = int(n.days/30)
    
    #Calculo del tiempo total de operacion del sistema
    tT = tiempo_total(Q, Lb)
    
    #Calculo de los costos por separado
    CO = PE*RC*tT
#    CA = (tT/(VUE*3600))*PA*(1+n)**I
    CA = (tT/(VUE*3600))*PA
    CW = PW*Lb
#    CM = (tT/FM)*PM*(1+n)**I
    CM = (tT/(FM*3600))*PM
    
    #Calculo del costo de riego total
    CR = CO+CA+CW+CM+CP
    
    if Lb == 0:
        CR = 0
    
    variables['CR'] = CR
    intercambio_variables.exp_var(variables)



