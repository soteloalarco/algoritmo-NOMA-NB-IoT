import numpy as np
import math as mth
import random
import operator
import copy

class Simulacion(object):
    def __init__(self, num_dispositivosU, num_dispositivosM, umbralArribos, PLE, r_cell):
        self.num_dispositivosU = num_dispositivosU  #Número dispositivos URLLC
        self.num_dispositivosM = num_dispositivosM  #Número dispositivos MTC
        self.umbralArribos = umbralArribos          #Umbral de arribos para paro de la simulación
        self.PLE = PLE       #Path Loss Exponent
        self.r_cell = r_cell #Radio de la celula
