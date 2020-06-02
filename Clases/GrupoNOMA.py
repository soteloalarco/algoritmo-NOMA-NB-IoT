import numpy as np
import math as mth
import random
import operator
import copy

class GrupoNOMA(object):
    def __init__(self, id, dispositivos, Ru, Rm, RTotal, gamma, Sac):
        self.id = id        # Identificador de Grupo
        self.dispositivos = dispositivos    #Lista de dispositivos agrupados en orden
        self.Ru = Ru            #Tasa de transmisión de dispositivos URLLC acumulada por grupo
        self.Rm = Rm            #Tasa de transmisión de dispositivos MTC acumulada por grupo
        self.RTotal = RTotal    #RTotal acumula las tasas de cada dispositivo por grupo y asi obtener la tasa alcanzada por grupo
        self.gamma = gamma      #Variable binaria que indica la asignación de un cluster para una subportadora
        self.Sac = Sac      #Conjunto de subportadoras asignadas a un cluster C
        #self.Sac_Cns = Sac_Cns  #Conjunto de subportadoras asignadas a un cluster Cns


