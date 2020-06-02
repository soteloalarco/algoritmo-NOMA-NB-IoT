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
DESsim = Simulacion(0, 3, 500)
NBIoT = NB_IoT(48, [], [], mth.sqrt(np.random.uniform(.1e3, 20e3)), mth.sqrt(np.random.uniform(.1e3, 2e3)), [], 48, [], 50, [], 150, [], 0, [], 4, 3.75e3, 5.012e-21)

#Creacion de Dispositivos URLLC
NBIoT.U.append(creardispositivos(NBIoT.numU, 1, DESsim.PLE, DESsim.r_cell, NBIoT.numS))
#Creacion de Dispositivos mMTC
NBIoT.M.append(creardispositivos(NBIoT.numM, 2, DESsim.PLE, DESsim.r_cell, NBIoT.numS))


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
            NBIoT.C.append(GrupoNOMA(deviceURLLC, [], 0, 0, 0, 1, []))
            NBIoT.C[deviceURLLC].dispositivos.append([NBIoT.U[0][deviceURLLC], False, False, False])
            NBIoT.U[0][deviceURLLC].alpha = 1
            indicePos1Grupo = indicePos1Grupo + 1
        else:
            # Si el número de dispositivos uRLLC [U] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
            # serán asignados a los siguientes rangos del grupo
            # TODO HARD CODED, sólo funciona para dispositivos entre 48 y 96
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
            #print('Se asignaron',deviceMTC, 'usuarios MTC pero eran ', NBIoT.numM, ' usuarios MTC' )
            break
    # Eliminar ceros que se agregaron a lista


    del NBIoT.M[0][0:cerosEliminar]

#Ejecución del algoritmo para la agrupación NOMA
AlgoritmoAgrupacion4NOMA()


#  *******************************************  Algoritmo para la asignación de recursos NOMA (subportadoras) **********************************************
def AlgoritmoAsignacionRecursos():

    # Conjunto de clusters de dispositivos con tasas insatisfechas
    NBIoT.Cns = copy.deepcopy(NBIoT.C)

    #Creacion de Subportadoras NB_IoT
    for s in range(0, NBIoT.numS):
        NBIoT.S.append(Subportadora(s, 0, []))

    #Inicio del bucle del algoritmo de asignación de recursos
    #while True:
        #Condiciones a cumplir para la asignacion de subportadoras
        #condicion1 = validacionTasasURLLC()
        #condicion2 = validacionTasasmMTC()
        #if (len(S) == 48) and (condicion1) and (condicion2):
        #    break
    # For para recorrer las 48 subportadoras
    for subportadora in range(0, NBIoT.numS):
        #For para recorrer los grupos no asignados de Cns
        NBIoT.id_c = False
        NBIoT.c_ = []
        for cluster in range(0, NBIoT.numC):
            # For para recorrer los rangos del grupo
            NBIoT.Cns[cluster].RTotal = 0
            for device in range(0, NBIoT.kmax):

                # Si es tipo URLLC
                R = 0
                if NBIoT.Cns[cluster].dispositivos[0][device].tipo == 1:
                    Interferencias = calculoInterferencia(subportadora, cluster, device)
                    R = NBIoT.Cns[cluster].gamma * NBIoT.BW * mth.log2(1 + (((abs(NBIoT.Cns[cluster].dispositivos[0][device].h[subportadora]) ** 2) * (NBIoT.Cns[cluster].dispositivos[0][device].Px)) / ((NBIoT.No * NBIoT.BW) + Interferencias)))
                    # Se asigna la tasa lograda a dispositivo URLLC
                    NBIoT.Cns[cluster].dispositivos[0][device].Rb = R

                # Si es tipo mMTC
                elif NBIoT.Cns[cluster].dispositivos[0][device].tipo == 2:
                    Interferencias = calculoInterferencia(subportadora, cluster, device)
                    R = NBIoT.Cns[cluster].gamma * NBIoT.BW * mth.log2(1 + (((abs(NBIoT.Cns[cluster].dispositivos[0][device].h[subportadora]) ** 2) * (NBIoT.Cns[cluster].dispositivos[0][device].Px)) / ((NBIoT.No * NBIoT.BW) + Interferencias)))
                    # Se asigna la tasa lograda a dispositivo MTC
                    NBIoT.Cns[cluster].dispositivos[0][device].Rb = R
                NBIoT.Cns[cluster].RTotal = NBIoT.Cns[cluster].RTotal + R

        #Grupo NOMA que maximiza la tasa
        NBIoT.id_c = busquedaMejorGrupoNOMA()
        #Actualización de variable binaria gamma
        NBIoT.Cns[NBIoT.id_c].gamma = 1
        #Asignación de subportadora a cluster de acuerdo con c*
        NBIoT.S[subportadora].idGrupo = NBIoT.id_c
        NBIoT.S[subportadora].GrupoNOMA = NBIoT.c_
    #Actualizar lista de subportadoras asignadas al cluster Sac

    #Actualizar lista de S' (Sv)

    #Actualización de Tasas del mejor grupo NOMA

    #Actualización de Potencias del mejor grupo NOMA

    #Validación del cumplimiento de tasas del grupo NOMA
        #Quitar o limpiar el mejor grupo de la lista Cns
        #Asignación de grupo a subportadora

    #Quitar o limpiar la subportadora S' (Sv) de conjunto S

    #Validación del cumplimiento de tasas del grupo NOMA
        #For para recorrer las Subportadoras
        #Encontrar mejor grupo NOMA para cada S
        #Modificar su gamma
        #Actualizar su Sac
    #Actualizar Potencias de:
    #FIN

#Funciones que se utilizan en algoritmo de asignación de recursos

#Calcula la Interferencia de los dispositivos del grupo NOMA para un dispositivo
def calculoInterferencia(subportadora, cluster, disp):
    Interference = 0
    #Se buscan dispositivos del mimsmo grupo pero con rangos superiores para calcular su contribución de interferencia
    for device in range(disp+1, NBIoT.kmax):
        I = (abs(NBIoT.Cns[cluster].dispositivos[0][device].h[subportadora]) ** 2) * (NBIoT.Cns[cluster].dispositivos[0][device].Px)
        Interference = Interference + I
    return Interference

def busquedaMejorGrupoNOMA():
    # Se busca el grupo que mejor maximize la tasa de acuerdo con Rtotal
    buscargrupo = max(GrupoNOMA.RTotal for GrupoNOMA in NBIoT.Cns)
    for cluster in range(0, NBIoT.numC):
        #Se busca el identificador del mejor grupo
        if NBIoT.Cns[cluster].RTotal == buscargrupo:
            break
    #Asignación de c*
    NBIoT.c_ = NBIoT.Cns[cluster]
    return NBIoT.Cns[cluster].id


#def validacionTasasURLLC():

AlgoritmoAsignacionRecursos()