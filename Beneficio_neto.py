#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 15:40:49 2019

@author: diego
"""
import pickle
import intercambio_variables

def BN_Incremental(variables):
    
    #Lectura de variables
    CHP = variables['CHP']
    PP = variables['PP']
    InYf = variables['InYf']
    Kif = variables['Kif']
    CR = variables['CR']
    #Incremento en la ganancia al vender el producto
    GP = (PP*InYf*Kif)/(1-CHP/100.0)

    #Beneficio neto para el intervalo considerado
    BN = GP - CR
    
    variables['GP'] = GP
    variables['BN'] = BN
    intercambio_variables.exp_var(variables)
