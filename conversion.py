#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 14:38:34 2019

@author: diego
"""

def gpm_ms(x):
    return (x*3.78/(1000*60))

def dia_seg(x):
    return(x*86400.0)

def hora_seg(x):
    return(x*3600.0)
    
def mm_m(x):
    return(x/1000.0)
    
def no_conversion(x):
    return(x)
    
def porc_dec(x):
    return(x/100)