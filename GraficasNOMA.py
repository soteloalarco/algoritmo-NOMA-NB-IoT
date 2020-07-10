#Importación de librerías
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
import subprocess
import sys
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import re
# Parallelizing using Pool.apply()
import multiprocessing as mp
from scipy.special import factorial

class Simulacion():
    a = []
    y = []
    y1 = []

# Simulacion para un conjunto de valores de a
def simulacion(a1):
    output = subprocess.check_output('NOMA_Algorithm.py '+str(a1), shell=True)
    output = output.decode(sys.stdout.encoding)
    return output.rstrip()


# Graficas NOMA
def Graficas(simulacion):
    plt.figure(100)
    plt.plot(simulacion.a, promedio, 'b', label="Resultados Simulación")
    y1 = [5e5, 8e5, 9.7e5, 11.6e5, 12.5e5]
    #y1 = [25,50, 75,100, 120, 125, 135, 140]
    plt.plot(simulacion.a, y1, 'r', label="Resultados Articulo")

    plt.xlabel('Numero de usuarios')
    plt.ylabel('Sum Rate (bps)')
    plt.title("NOMA con 48 subportadoras y 48 clusters, con agrupamientos de 4 usuarios")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)

    plt.show()



if __name__ == '__main__':
    # Definicion de Parámetros de la simulación
    output = []

    simulacion = Simulacion()  # Creación de objeto de clase Simulación
    #simulacion.a = [25,50,75,100,125,150,175,192]
    simulacion.a = [10,20,30,40,50]
    # os.system('cls')
    inicio = timer()
    print("  Simulando  ...")

    simulacion.y=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    #simulacion.y = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    #simulacion.y1=[0,0,0,0,0,0,0,0]
    simulacion.y1 = [0,0,0,0,0]
    rep = 100

    for reps in range (0, rep):
        # Multiprocesamiento
        pool = mp.Pool(mp.cpu_count())
        results = pool.map(simulacion, [a1 for a1 in simulacion.a])
        pool.close()

        #Conversion del formato de salida
        for i in range(len(results)):
           simulacion.y[reps].append(float(results[i]))

        #Graficas(simulacion)

    for rep1 in range(0,rep):
        for valor in range(0, 5):
            simulacion.y1[valor] = simulacion.y1[valor] + simulacion.y[rep1][valor]

    promedio=[]
    promedio= [x / rep for x in simulacion.y1]
    promedio
    Graficas(simulacion)
    fin = timer()
    tiempo_TotalSimulacion = fin - inicio

    print('Tiempo total de simulacion en segundos: ', tiempo_TotalSimulacion, '  en minutos: ', tiempo_TotalSimulacion/60, '  y en horas: ', tiempo_TotalSimulacion/60/60)
