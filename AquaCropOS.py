#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:51:05 2019

@author: diego
"""

import os
import intercambio_variables
from datetime import datetime
from datetime import timedelta

def init_irrigation(variables, zero=False, loop = True):
    FILES_PATH = variables['FILES_PATH']
    f = open(os.path.join(FILES_PATH, 'IrrigationSchedule.txt'), 'r')
    IrrigationSchedulle = f.readlines()
    f.close()
    l = len(IrrigationSchedulle)
    #Si quiero borrar todas las aplicaciones anteriores
    if zero:
        IrrigationSchedulle = IrrigationSchedulle[0:2]
    #Para conservar las aplicaciones anteriores
    elif loop:
        IrrigationSchedulle = IrrigationSchedulle[0:l-1]
    else:
        IrrigationSchedulle = IrrigationSchedulle
    f = open(os.path.join(FILES_PATH, 'IrrigationSchedule.txt'), 'w')
    for i in IrrigationSchedulle:
        f.write(i)
    f.close()
    
def set_irrigation(variables):
    FILES_PATH = variables['FILES_PATH']
    D = variables['D']
    Ln = variables['Ln']
    f = open(os.path.join(FILES_PATH, 'IrrigationSchedule.txt'), 'r')
    IrrigationSchedulle = f.readlines()
    IrrigationSchedulle.append(datetime.strftime(D, '%d')+ '\t' + 
                               datetime.strftime(D, '%m')+ '\t' + 
                               datetime.strftime(D, '%Y')+ '\t' + 
                               str(int(Ln)) + '\r\n')
    f.close()
    f = open(os.path.join(FILES_PATH, 'IrrigationSchedule.txt'), 'w')
    for i in IrrigationSchedulle:
        f.write(i)
    f.close()
    
#Modifica los archivos Clock y CropRotation para configurar las fechas de simulacion
#Siembra y cosecha
def set_clock(CropName, variables):
    FILES_PATH = variables['FILES_PATH']
    FeSi = variables['FeSi']
    FeCo = variables['FeCo']
    f = open(os.path.join(FILES_PATH, 'Clock.txt'), 'r')
    Clock = f.readlines()
    f.close()
    Clock[2] = 'SimulationStartTime : ' + datetime.strftime(FeSi, '%Y-%m-%d') + '\r\n'
    Clock[4] = 'SimulationEndTime : ' + datetime.strftime((FeCo), '%Y-%m-%d') + '\r\n'
    f = open(os.path.join(FILES_PATH, 'Clock.txt'), 'w')
    for i in Clock:
        f.write(i)
    f.close()
    f = open(os.path.join(FILES_PATH, 'CropRotation.txt'), 'r')
    CropRotation = f.readlines()
    f.close()
    CropRotation[2] = (datetime.strftime(FeSi, '%d/%m/%Y') + '\t' + 
                datetime.strftime(FeCo, '%d/%m/%Y') + '\t' + CropName + '\r\n')
    f = open(os.path.join(FILES_PATH, 'CropRotation.txt'), 'w')
    for i in CropRotation:
        f.write(i)
    f.close()
    
    