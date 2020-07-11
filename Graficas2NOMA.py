#Este script realiza la simulacion M/M tomando como métrica de paro un número tope de arribos
#Importación de librerías
import os
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
import subprocess
import sys
import re
import multiprocessing as mp
import math as mth



# Simulacion para un conjunto de valores de a
class Simulacion():
    """Esta clase representa una simulación"""
    a = []
    y = []
    y2=[]
    y1=[]
    numceldas = 0
    numMetricas = []
    Metricas = {}
    areaTotal =0

# Simulacion para un conjunto de valores de a
def simulacion_a(a1):
    #Conversion del formato de salida
    output = subprocess.check_output('NOMA_Algorithm.py '+str(a1), shell=True)
    output1 = output.decode(sys.stdout.encoding)
    output2 = str((re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', output1)).rstrip()).split(" , ")
    output3 = np.array(output2, float)
    return output3


def creacionDiccionarios(simulacion):
    for x in range(0,simulacion.numMetricas):
        simulacion.Metricas["Metrica"+str(x)] = []


def Graficas(simulacion):
    plt.figure(2)

    simulacion.y1 = np.array(simulacion.Metricas['Metrica' + str(0)][0])
    simulacion.y2 = np.array(simulacion.Metricas['Metrica' + str(1)][0])

    #plt.plot(simulacion.a, simulacion.y, '-rD', label="mMTC")
    #plt.plot(simulacion.a,simulacion.y2, '-bD', label="uRLLC")
    plt.bar(simulacion.a, promedioM, width=10, align='center', label="mMTC")
    plt.bar(simulacion.a,promedioU, width=10, align='center', label="uRLLC")
    plt.xlabel('Número de usuarios')
    plt.ylabel('Número de usuarios \n con tasas satisfechas')
    plt.title("NB-IoT $Singletone$")
    plt.legend(loc='best', borderaxespad=0.)

    plt.show()





if __name__ == '__main__':
    # Definicion de Parámetros de la simulación
    capacidad = 0
    output = []
    z = []
    Z = []
    URLLC=[]
    MTC=[]
    simulacion = Simulacion()  # Creación de objeto de clase Simulación
    simulacion.numMetricas = 2

    simulacion.a = [25,50,75,100,125,150,175,192]
    promedioMTC=[0,0,0,0,0,0,0,0]
    promedioURLLC = [0,0,0,0,0,0,0,0]
    inicio = timer()
    print("  Simulando  ...")
    # Multiprocesamiento

    rep=10
    for reps in range(0,rep):
        pool = mp.Pool(mp.cpu_count())

        results = pool.map(simulacion_a, [a1 for a1 in simulacion.a])

        pool.close()

        creacionDiccionarios(simulacion)
        for i in range(0, simulacion.numMetricas):
            Z=[]
            for j in range(0, len(results)):
                Z.append(results[j][i])
            simulacion.Metricas['Metrica' + str(i)].append(Z)

        MTC.append(np.array(simulacion.Metricas['Metrica' + str(0)][0]))
        URLLC.append(np.array(simulacion.Metricas['Metrica' + str(1)][0]))

    for rep1 in range(0, rep):
        for valor in range(0, len(simulacion.a)):
            promedioMTC[valor] = promedioMTC[valor] + MTC[rep1][valor]
    for rep1 in range(0, rep):
        for valor in range(0, len(simulacion.a)):
            promedioURLLC[valor] = promedioURLLC[valor] + URLLC[rep1][valor]


    promedioM= [x / rep for x in promedioMTC]
    promedioU = [x / rep for x in promedioURLLC]
    Graficas(simulacion)


    fin = timer()
    tiempo_TotalSimulacion = fin - inicio
    print('Tiempo total de simulacion en segundos: ', tiempo_TotalSimulacion, '  en minutos: ', tiempo_TotalSimulacion/60, '  y en horas: ', tiempo_TotalSimulacion/60/60)

