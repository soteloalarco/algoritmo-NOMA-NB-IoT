import numpy as np
import math as mth
import random
import operator
import copy
from Clases.GrupoNOMA import  GrupoNOMA
from Clases.Subportadora import Subportadora
from Clases.NB_IoT import NB_IoT
from Clases.Simulacion import Simulacion
from Clases.Dispositivo import Dispositivo



def creardispositivos(numeroDispositivos, tipo, PLE, radio_celula, numeroSubportadoras):
    dispositivos = []
    for disp in range(0, numeroDispositivos):  # Generamos la cantidad indicada de dispositivos de cada tipo

        h2 = 0
        for gain in range(0, numeroSubportadoras):
            # Usuarios uniformemente distribuidos dentro de la celda entre .1 a 500m
            d = mth.sqrt(np.random.uniform(0, 1) * (radio_celula ** 2))
            ple = PLE
            #Implementacion de desvanecimiento tipo Rayleigh
            rayleighGain = random.expovariate(1)
            h1 = (d ** (-ple)) * rayleighGain
            h2 = h2 + h1
        h = h2 / numeroSubportadoras

        dispositivos.append(Dispositivo(disp, tipo, 0, h, 0, .2))

    # Ordenamiento de dispositivos con base en sus ganancia promedio de canal (descendentemente)
    dispositivosorted = sorted(dispositivos, key=operator.attrgetter('h'), reverse=True)
    return dispositivosorted


