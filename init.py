#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 16:41:58 2019

@author: diego
"""

#import cultivo
#import Beneficio_neto
#import riego
import os
os.chdir('/home/diego/Documentos/Maestría/Tesis/Scripts/Metodologia')

import numpy as np
import pandas as pd
import intercambio_variables
import AquaCropOS
import riego
import cultivo
import Beneficio_neto
from datetime import datetime
from datetime import timedelta

#Funcion para imprimir el numero legible
def place_value(number): 
    return ("{:,}".format(number)) 

#Cargo los parámetros
variables = intercambio_variables.init_variables()
variables = intercambio_variables.leer_variables(variables)

#Defino las fechas como formato de fecha
variables['FISR'] = datetime.strptime(variables['FISR'], '%Y-%m-%d')
variables['FeSi'] = datetime.strptime(variables['FeSi'], '%Y-%m-%d')
variables['FeAc'] = datetime.strptime(variables['FeAc'], '%Y-%m-%d')
variables['FeCo'] = datetime.strptime(variables['FeCo'], '%Y-%m-%d')
variables['FeFP'] = variables['FeAc'] + timedelta(days = 6)
intercambio_variables.exp_var(variables)
#Configuro las fechas de simulación 
AquaCropOS.set_clock('Papa', variables)

#Defino la lista de láminas a aplicar
L_list = np.arange(0,variables['LnX']+1) 

#Listas de variables a considerar en cada iteración
D_list = []
Ln_list = []
BN_list = []
GP_list = []
CR_list = []
YSd_list = []
Biof_list = []
#Inicio el archivo de riegos, conservando los riegos que ya están definidos
AquaCropOS.init_irrigation(variables, loop = False)
#Hora de inicio de la corrida
hora_inicio = datetime.strftime(datetime.now(), '%H:%M:%S')
for j in range(7):
#Defino o modifico el día de la aplicación
    variables['D'] = variables['FeAc'] + timedelta(days = j)
    for lamina in L_list:
        #Defino o modifico el valor de la lámina
        variables['Ln'] = lamina
        #Añado la aplicación de riego
        AquaCropOS.set_irrigation(variables)
        #Exporto variables
        intercambio_variables.exp_var(variables)
        #Corro el modelo
        os.chdir(variables['AQUACROP_PATH'])
        os.system('octave AquaCropOS_RUN.m')
        print('Corrida ' + datetime.strftime(variables['D'], '%Y-%m-%d') + 
              ' lamina ' + str(lamina) + 'mm')
        os.chdir('/home/diego/Documentos/Maestría/Tesis/Scripts/Metodologia')
        #Calculo de los costos de riego
        riego.Costo_Riego(variables)
        variables = intercambio_variables.imp_var()
        #Calculo de la ganancia incremental del cultivo
        cultivo.Incremento_Produccion(variables)
        variables = intercambio_variables.imp_var()
        #Si el cultivo aun no germina no calcula nada
        if variables['Germ']:
            #Calculo del beneficio neto
            Beneficio_neto.BN_Incremental(variables)
            variables = intercambio_variables.imp_var()
            print('Beneficio Neto Incremental = $' + str(place_value(int(variables['BN']))))
            print('Kif= ' + str(round(variables['Kif'],2)) + '\t' + 'InYf= ' + 
                  str(round(variables['InYf'],2)))
        else:
            print('El cultivo aun no emerge')
        BN_list.append(variables['BN'])
        GP_list.append(variables['GP'])
        CR_list.append(variables['CR'])
        D_list.append(variables['D'])
        Biof_list.append(variables['Biof'])
        YSd_list.append(variables['YSd'])
        Ln_list.append(lamina)
        AquaCropOS.init_irrigation(variables)

DF = pd.DataFrame({'BN':BN_list, 'GP':GP_list, 'CR':CR_list, 'Ln':Ln_list, 'D':D_list, 
                   'Biof':Biof_list, 'YSd':YSd_list})
DF.to_csv('Graphs/Resultados_Corrida_'+datetime.strftime(variables['FeAc'], '%Y%m%d')+'.csv')

#La desviación estandar del rendimiento en ese periodo
if variables['Germ']:
    YSd = np.mean(variables['YSd'])
    #Si YSd < 0.05 la formación del rendimiento aún no inicia completamente
    #Y la optimización se hace con respecto a la biomasa
    if YSd < 0.05:
        Op_index = DF.loc[DF['Biof'] == DF['Biof'].max()].index
    else:
        Op_index = DF.loc[DF['BN'] == DF['BN'].max()].index
    Op_index = Op_index[0] #EL primer index debe ser la menor lámina

    print('La aplicacion de riego optima es de ' + str(DF['Ln'][Op_index]) + 'mm el '
          + datetime.strftime(DF['D'][Op_index], '%d-%m-%Y'))
if variables['Cosecha']:
    print('Cosecha estimada para el ' + datetime.strftime(variables['FeCo'], "%d-%m-%Y"))        
print('Hora de inicio : ' + hora_inicio)
print('Hora de finalizacion :' + datetime.strftime(datetime.now(), '%H:%M:%S') )