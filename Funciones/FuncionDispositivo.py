import numpy as np
import math as mth
import random
import operator
from Clases.Dispositivo import Dispositivo

def creardispositivos(numeroDispositivos, tipo, PLE, radio_celula, numeroSubportadoras):

    dispositivos = []
    for disp in range(0, numeroDispositivos):  # Generamos la cantidad indicada de dispositivos de cada tipo

        #Creación de ganancias por cada subportadora
        h = []
        for gain in range(0, numeroSubportadoras):
            # Usuarios uniformemente distribuidos dentro de la celda entre .1 a 500m
            ple = PLE
            #Implementacion de desvanecimiento tipo Rayleigh
            rayleighGain = random.expovariate(1)

            # Calculo de distancia del UE a la BS
            d = mth.sqrt(np.random.uniform(0, 1) * (radio_celula ** 2))
            h.append((d ** (-ple)) * rayleighGain)
        h2 = sum(h)
        #Ganancia Promedio
        h_ = h2 / numeroSubportadoras

        #Asignación de potencias para cada subportadora
        Px = []
        for power in range(0, numeroSubportadoras):
            Px.append(.2)

        #Asignación de umbrales de tasa de transmisión dependiendo el tipo de dispositivo
        if tipo == 1:
            Rth = np.random.uniform(100, 20e3)
        elif tipo == 2:
            Rth = np.random.uniform(100, 2e3)

        #Se crea el dispositivo de acuerdocon las caracteristicas establecidas
        dispositivos.append(Dispositivo(disp, tipo, 0, h_, h, 0, Px, Rth))

    # Ordenamiento de dispositivos con base en sus ganancia promedio de canal (descendentemente)
    dispositivosorted = sorted(dispositivos, key=operator.attrgetter('h_'), reverse=True)
    return dispositivosorted
