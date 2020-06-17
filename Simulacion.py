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
    """Esta clase representa una simulación"""
    a = []
    y = []

# Simulacion para un conjunto de valores de a
def simulacion_a(a1):
    output = subprocess.check_output('NOMA_Algorithm.py '+str(a1), shell=True)
    output = output.decode(sys.stdout.encoding)
    return output.rstrip()


# Graficas de Probabilidad de Bloqueo
def graficasProbBloq(simulacion):
    plt.figure(100)
    plt.plot(simulacion.a, simulacion.y, 'g', label="kmax=4")

    plt.xlabel('Numero de usuarios')
    plt.ylabel('Usuarios con tasas satisfechas')
    plt.title("NOMA con clusters y subportadoras de 48")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)

    plt.show()





if __name__ == '__main__':
    # Definicion de Parámetros de la simulación
    capacidad = 0
    umbralTopeArribos = 0
    output = []

    simulacion = Simulacion()  # Creación de objeto de clase Simulación
    simulacion.a = [25,50,75,100,125,150,175,200]
    # os.system('cls')
    inicio = timer()
    print("  Simulando  ...")
    # Multiprocesamiento

    pool = mp.Pool(mp.cpu_count())

    results = pool.map(simulacion_a, [a1 for a1 in simulacion.a])

    pool.close()

    #Conversion del formato de salida

    for i in range(len(results)):
       simulacion.y.append(int(results[i]))

    graficasProbBloq(simulacion)


    fin = timer()
    tiempo_TotalSimulacion = fin - inicio
    print('Tiempo total de simulacion en segundos: ', tiempo_TotalSimulacion, '  en minutos: ', tiempo_TotalSimulacion/60, '  y en horas: ', tiempo_TotalSimulacion/60/60)
