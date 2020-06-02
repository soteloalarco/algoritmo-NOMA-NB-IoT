import numpy as np
import math as mth
import random
import operator
import copy
from Clases.Dispositivo import Dispositivo



def creardispositivos(numeroDispositivos, tipo, PLE, radio_celula):
    dispositivos = []
    for disp in range(0, numeroDispositivos):  # Generamos la cantidad indicada de dispositivos de cada tipo
        # Usuarios uniformemente distribuidos dentro de la celda entre .1 a 500m
        d = mth.sqrt(np.random.uniform(0, 1) * (radio_celula ** 2))
        ple = PLE
        #Implementacion de desvanecimiento tipo Rayleigh
        rayleighGain = random.expovariate(1)
        #TODO calcular 48 y sacar el promedio
        h = (d ** (-ple)) * rayleighGain
        dispositivos.append(Dispositivo(disp, tipo, 0, d, h, 0, .2))

    # Ordenamiento de dispositivos con base en sus ganancias de canal (descendentemente)
    dispositivosorted = sorted(dispositivos, key=operator.attrgetter('h'), reverse=True)
    return dispositivosorted
