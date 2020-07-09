import numpy as np
import math as mth
import random
import operator
from scipy.stats import expon
from Clases.Dispositivo import Dispositivo

def creardispositivos(numeroDispositivos, tipo, PLE, radio_celula, numeroSubportadoras):

    dispositivos = []
    for disp in range(0, numeroDispositivos):  # Generamos la cantidad indicada de dispositivos de cada tipo

        #Creación de ganancias por cada subportadora
        h = []
        # Usuarios uniformemente distribuidos dentro de la celda entre .1 a 500m
        # Calculo de distancia del UE a la BS
        d = mth.sqrt(np.random.uniform(0, 1) * (radio_celula ** 2))
        ple = PLE

        for gain in range(0, numeroSubportadoras):
            #Implementacion de desvanecimiento tipo Rayleigh
            #rayleighGain = expon.rvs(loc=0, scale=1, size=1, random_state=None)
            #rayleighGain = np.random.rayleigh(scale=1.0, size=None)
            rayleighGain = random.expovariate(1)
            h.append((d ** (-ple)) * rayleighGain)
        h2 = sum(h)

        #Ganancia Promedio
        h_ = h2 / numeroSubportadoras

        #Asignación de potencias para cada subportadora
        Px = []
        #Asignación de umbrales de tasa de transmisión dependiendo el tipo de dispositivo
        if tipo == 1:
            for power in range(0, numeroSubportadoras):
                Px.append(.2)
            Rth = np.random.uniform(100, 20e3)
        elif tipo == 2:
            for power in range(0, numeroSubportadoras):
                Px.append(.1)
            Rth = np.random.uniform(100, 2e3)

        #Se crea el dispositivo de acuerdo con las caracteristicas establecidas
        dispositivos.append(Dispositivo(disp, tipo, 0, d, h_, h, 0, 0, Px, Rth))

    # Ordenamiento de dispositivos con base en sus ganancia promedio de canal (descendentemente)
    dispositivosorted = sorted(dispositivos, key=operator.attrgetter('h_'), reverse=True)
    return dispositivosorted
