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
def simulacionNOMA(a1):
    output = subprocess.check_output('NOMA_Algorithm.py '+str(a1), shell=True)
    output = output.decode(sys.stdout.encoding)
    return output.rstrip()


# Graficas NOMA
def Graficas(simulacion):
    plt.figure(100)
    #y1 = [5e5, 8e5, 9.7e5, 11.6e5, 12.5e5]
    y1 = [25, 50, 75, 100, 120, 126, 135, 140]
    plt.plot(simulacion.a, y1, '-gD', label="Resultados Artículo")
    plt.plot(simulacion.a, promedio, '-cD', label="Resultados Simulación")
    #plt.ylim((3e5, 2.5e7))
    #plt.ylim((0, 2,5e7))
    plt.xlabel('Número de usuarios')
    plt.ylabel('Número de usuarios promedio \n con tasas satisfechas')
    plt.title("NB-IoT $Multitone$")
    plt.legend(loc='best', borderaxespad=0.)

    plt.show()

#Singletone
#[23.295, 46.36, 60.14, 74.895, 87.99, 99.085, 110.035, 117.725]

#Multitone
#[24.35, 45.08, 61.945, 74.93, 88.395, 94.36, 107.905, 117.225]

if __name__ == '__main__':
    # Definicion de Parámetros de la simulación
    output = []

    simulacion = Simulacion()  # Creación de objeto de clase Simulación
    simulacion.a = [25,50,75,100,125,150,175,192]
    #simulacion.a = [10,20,30,40,50]
    # os.system('cls')
    inicio = timer()
    print("  Simulando  ...")

    simulacion.y=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[], [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    #simulacion.y = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    simulacion.y1=[0,0,0,0,0,0,0,0]
    #simulacion.y1 = [0,0,0,0,0]
    rep = len(simulacion.y)

    for reps in range (0, rep):
        # Multiprocesamiento
        pool = mp.Pool(mp.cpu_count())
        results = pool.map(simulacionNOMA, [a1 for a1 in simulacion.a])
        pool.close()

        #Conversion del formato de salida
        for i in range(len(results)):
           simulacion.y[reps].append(float(results[i]))

        #Graficas(simulacion)

    for rep1 in range(0,rep):
        for valor in range(0, len(simulacion.a)):
            simulacion.y1[valor] = simulacion.y1[valor] + simulacion.y[rep1][valor]

    promedio=[]
    promedio= [x / rep for x in simulacion.y1]
    promedio
    Graficas(simulacion)
    fin = timer()
    tiempo_TotalSimulacion = fin - inicio

    print('Tiempo total de simulacion en segundos: ', tiempo_TotalSimulacion, '  en minutos: ', tiempo_TotalSimulacion/60, '  y en horas: ', tiempo_TotalSimulacion/60/60)
