import numpy as np
import math as mth
import random
import operator
import copy

class Dispositivo(object):
    #Constructor
    def __init__(self, id, tipo, alpha, h, Rb, Px):
        self.id = id        #Identificador de dispositivo
        self.tipo = tipo    #Tipo de Dispositivo
        self.alpha = alpha    #Variable binaria que indica si el dispositivo esta agrupado en un cluster NOMA
        #self.d = d          #Distancia entre BS y UE
        self.h = h          #Ganancia de canal
        self.Rb = Rb        #Tasa de transmisión
        self.Px = Px        #Potencia de transmisión


