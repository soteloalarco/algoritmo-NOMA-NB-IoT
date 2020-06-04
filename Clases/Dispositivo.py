import numpy as np
import math as mth
import random
import operator
import copy

class Dispositivo(object):
    #Constructor
    def __init__(self, id, tipo, alpha, h_, h, Rb, Px, Rth):
        self.id = id        #Identificador de dispositivo
        self.tipo = tipo    #Tipo de Dispositivo
        self.alpha = alpha    #Variable binaria que indica si el dispositivo esta agrupado en un cluster NOMA
        #self.d = d          #Distancia entre BS y UE
        self.h_ = h_        #Ganancia de canal promedio
        self.h = h          #Ganancias de canal por subportadora
        self.Rb = Rb        #Tasa de transmisión
        self.Px = Px        #Potencia de transmisión
        self.Rth = Rth    #Umbral de tasa para dispositivos


