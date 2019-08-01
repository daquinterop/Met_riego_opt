#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:30:42 2019

@author: diego
"""

import pickle
import pandas as pd
from conversion import no_conversion as nc
from conversion import hora_seg 
from conversion import porc_dec
from conversion import gpm_ms 
from conversion import mm_m



#Funcion que inicia el dict con variables
def init_variables():
    variables = { 'Kif':None, 'InYf':None, 'CR':None, 'PP':None, 'FeSi':None, 
                 'FeAc':None, 'FeFP':None, 'PATH_AC_OUT':None, 'PROJECT_NAME':None,
                 'Ktrx':None, 'KtrMean':None, 'FISR':None, 'Q':None, 'PE':None,
                 'RC':None, 'VUE':None, 'PA':None, 'PW':None, 'FM':None,
                 'PM':None, 'CP':None, 'GP':None, 'BN':None, 'CHP':None, 'Ln':None,
                 'D':None, 'LnX':None, 'Ef':None, 'I':None, 'AQUACROP_PATH':None,
                 'FILES_PATH':None, 'FeCo':None, 'Biof':None, 'YSd':None, 
                 'Cosecha':None, 'Germ':None}
    return(variables)

#Lectura de las variables
def leer_variables(variables, nombre = 'variables.csv'):
    #Tipo de las variables de entrada
    var_type = { 'Kif':float, 'InYf':float, 'CR':float, 'PP':float, 'FeSi':str, 
                 'FeAc':str, 'FeFP':str, 'PATH_AC_OUT':str, 'PROJECT_NAME':str,
                 'Ktrx':float, 'KtrMean':float, 'FISR':str, 'Q':float, 'PE':float,
                 'RC':float, 'VUE':float, 'PA':float, 'PW':float, 'FM':float,
                 'PM':float, 'CP':float, 'GP':float, 'BN':float, 'CHP':float, 'Ln':float,
                 'D':float, 'LnX':float, 'Ef':float, 'I':float, 'AQUACROP_PATH':str,
                 'FILES_PATH':str, 'FeCo':str, 'Biof':float, 'YSd':float, 
                 'Cosecha':bool, 'Germ':bool}
    var_conv = { 'Kif':nc, 'InYf':nc, 'CR':nc, 'PP':nc, 'FeSi':nc, 
                 'FeAc':nc, 'FeFP':nc, 'PATH_AC_OUT':nc, 'PROJECT_NAME':nc,
                 'Ktrx':nc, 'KtrMean':nc, 'FISR':nc, 'Q':gpm_ms, 'PE':nc,
                 'RC':nc, 'VUE':nc, 'PA':nc, 'PW':nc, 'FM':hora_seg,
                 'PM':nc, 'CP':nc, 'GP':nc, 'BN':nc, 'CHP':nc, 'Ln':mm_m,
                 'D':nc, 'LnX':nc, 'Ef':porc_dec, 'I':porc_dec, 'AQUACROP_PATH':nc,
                 'FILES_PATH':nc, 'FeCo':nc, 'Biof':nc, 'YSd':nc, 
                 'Cosecha':nc, 'Germ':nc}
    #Lee el archivo de entrada con las variables
    table = pd.read_table(nombre, sep='\t', index_col = 0)
    #Crea el archivo de variables
    for i in table.iterrows():
        variables[i[0]] = table['Valor'][i[0]]
    #Asigna cada variable su tipo
    for i in variables.iterkeys():
        if variables[i] != None:
            variables[i] = var_type[i](variables[i])
            variables[i] = var_conv[i](variables[i])
    return(variables)


#Exporta el objeto
def exp_var(x, name = 'kiosk'):
    filename = name +'.pi'
    outfile = open(filename, 'wb')
    pickle.dump(x, outfile)
    outfile.close

#Importa el objeto
def imp_var(name = 'kiosk'):
    infile = open(name+'.pi','rb')
    new_var = pickle.load(infile)
    infile.close()
    return(new_var)
