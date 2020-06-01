import sys
import simpy
import cmath as cmth
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon # Librería para dibujar los hexagonos
import pandas as pd
import numpy as np
import math as mth
import random
import operator
import copy
from operator import itemgetter, attrgetter, methodcaller
from Clases.Dispositivo import Dispositivo
from Clases.GrupoNOMA import  GrupoNOMA
from Clases.Subportadora import Subportadora
from Clases.NB_IoT import NB_IoT
from Funciones.FuncionDispositivo import creardispositivos
from Clases.Simulacion import Simulacion

#Creación de Objetos para la simulación
DESsim = Simulacion(144, 48, 0, 3, 500)
NBIoT = NB_IoT(48, [], [], mth.sqrt(np.random.uniform(.1, 20)) * 1e3, mth.sqrt(np.random.uniform(.1, 2)) * 1e3, [], 48, [], 50, [], 150, [], 0, [], 4, 3.75e3, 5.012e-21)

#Creacion de Dispositivos URLLC
NBIoT.U.append(creardispositivos(NBIoT.numU, 1, DESsim.PLE, DESsim.r_cell))
#Creacion de Dispositivos mMTC
NBIoT.M.append(creardispositivos(NBIoT.numM, 2, DESsim.PLE, DESsim.r_cell))


#  *******************************************  Algoritmo para el agrupamiento de dispositivos (clustering NOMA)  **********************************************
def AlgoritmoAgrupacion4NOMA():
    # Se empiezan a agrupar usuarios con una alta ganancia de canal promedio,
    # en la recepción tipo SIC se decodifican primero los usuarios con una alta ganancia de canal promedio antes que los de baja ganancia  de canal promedio
    # Los rangos de los dispositivos uRLLC deben ser menores que los MTC para que sea eficiente la decodificación SIC

    # j es la última posición de asignación de usuarios URLLC
    indicePos1Grupo = 0
    indicePos2Grupo = 0
    # AGRUPAMIENTO DE USUARIOS URLLC
    # Solo para grupos de 4 usuarios
    for deviceURLLC in range(0, int(NBIoT.numU)):
        # deviceURLLC corresponde al número de dispositivos uRLLC [U]
        if deviceURLLC < NBIoT.numC:
            # Asignar los dispositivos uRLLC a rangos bajos de los primeros grupos
            NBIoT.C.append(GrupoNOMA(deviceURLLC, [], 0, 0, 0, 4, 1, [], []))
            NBIoT.C[deviceURLLC].dispositivos.append([NBIoT.U[0][deviceURLLC], False, False, False])
            NBIoT.U[0][deviceURLLC].alpha = 1
            indicePos1Grupo = indicePos1Grupo + 1
        else:
            # Si el número de dispositivos uRLLC [U] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
            # serán asignados a los siguientes rangos del grupo
            NBIoT.C[indicePos2Grupo].dispositivos[0][1] = NBIoT.U[0][deviceURLLC]
            NBIoT.U[0][deviceURLLC].alpha = 1
            indicePos2Grupo = indicePos2Grupo + 1

    cerosEliminar = indicePos2Grupo

    indicePos3Grupo=0
    indicePos4Grupo=0
    #Agregar ceros a lista
    for g in range(0, indicePos2Grupo):
        NBIoT.M[0].insert(0, 0)

    # AGRUPAMIENTO DE USUARIOS mMTC
    # Solo para grupos de 4 usuarios
    for deviceMTC in range(indicePos2Grupo, int(NBIoT.numM)):
        # Si el número de dispositivos mMTC [M] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
        # serán asignados a los siguientes rangos del grupo, última posición de asignación
        if deviceMTC < (NBIoT.numC):
            # Asignar los dispositivos mmtc a los rangos mas bajos de los primeros grupos
            NBIoT.C[indicePos2Grupo].dispositivos[0][1] = NBIoT.M[0][deviceMTC]
            NBIoT.M[0][deviceMTC].alpha = 1
            indicePos2Grupo = indicePos2Grupo + 1
        elif deviceMTC < (2*NBIoT.numC):
            # Asignar los dispositivos mMTC a los siguientes rangos del grupo
            NBIoT.C[indicePos3Grupo].dispositivos[0][2] = NBIoT.M[0][deviceMTC]
            NBIoT.M[0][deviceMTC].alpha = 1
            indicePos3Grupo = indicePos3Grupo + 1
        elif deviceMTC < (3*NBIoT.numC):
            # Asignar los dispositivos mMTC a los siguientes rangos del grupo
            NBIoT.C[indicePos4Grupo].dispositivos[0][3] = NBIoT.M[0][deviceMTC]
            NBIoT.M[0][deviceMTC].alpha = 1
            indicePos4Grupo = indicePos4Grupo + 1
        else:
            print('Se asignaron',deviceMTC, 'usuarios MTC pero eran ', NBIoT.numM, ' usuarios MTC' )
            break
    # Eliminar ceros que se agregaron a lista
    del NBIoT.M[0][0:cerosEliminar]

#Ejecución del algoritmo para la agrupación NOMA
AlgoritmoAgrupacion4NOMA()