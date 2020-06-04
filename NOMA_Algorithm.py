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
NBIoT = NB_IoT(48, [], [], [], [], 48, [], 50, [], 150, [], 0, [], 4, 3.75e3, 5.012e-21)

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
            NBIoT.C.append(GrupoNOMA(deviceURLLC, [], False, 0, 0, 0, 1, [], []))
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
            #print('Se asignaron',deviceMTC, 'usuarios MTC pero eran ', NBIoT.numM, ' usuarios MTC' )
            break
    # Eliminar ceros que se agregaron a lista


    del NBIoT.M[0][0:cerosEliminar]

#Ejecución del algoritmo para la agrupación NOMA
AlgoritmoAgrupacion4NOMA()

#  *******************************************  Algoritmo para la asignación de recursos NOMA (subportadoras) **********************************************
def AlgoritmoAsignacionRecursos():
    NBIoT.Sv = 0
    # Conjunto de clusters de dispositivos con tasas insatisfechas
    NBIoT.Cns = copy.deepcopy(NBIoT.C)
    #Creacion de Subportadoras NB_IoT
    for s in range(0, NBIoT.numS):
        NBIoT.S.append(Subportadora(s, []))

    #Inicio del bucle del algoritmo de asignación de recursos
    while True:
        if (len(NBIoT.Clusters) == 48):
            break
        for i in range(0, NBIoT.numC):
            NBIoT.Cns[i].Sac = []
        # For para recorrer las 48 subportadoras
        for subportadora in range(0, NBIoT.numS):
            NBIoT.id_c = False
            NBIoT.c_ = []
            if NBIoT.S[subportadora].GrupoNOMA == []:
                # For para recorrer los grupos no asignados de Cns
                for cluster in range(0, NBIoT.numC):
                    #Validación de que el cluster ya esté asignado a una subportadora
                    if NBIoT.Cns[cluster].Subcarrier == []:
                        NBIoT.Cns[cluster].RTotal = 0
                        # For para recorrer los rangos del grupo
                        for device in range(0, NBIoT.kmax):
                            Interferencias = calculoInterferencia(subportadora, cluster, device)
                            R = calculoTasaTx(Interferencias, subportadora, cluster, device)
                            # Se asigna la tasa lograda a dispositivo URLLC
                            NBIoT.Cns[cluster].dispositivos[0][device].Rb = R
                            NBIoT.Cns[cluster].RTotal = NBIoT.Cns[cluster].RTotal + R

                #Grupo NOMA que maximiza la tasa
                NBIoT.id_c = busquedaMejorGrupoNOMA()
                #Actualización de variable binaria gamma
                NBIoT.Cns[NBIoT.id_c].gamma = 1

                #Actualizar lista de subportadoras asignadas al cluster Sac
                NBIoT.Cns[NBIoT.id_c].Sac.append(NBIoT.S[subportadora].id)
                #Actualizar lista de S' (Sv)
                #NBIoT.Sv.append(NBIoT.S[subportadora].id)

                Sac = NBIoT.Cns[NBIoT.id_c].Sac.count(NBIoT.S[subportadora].id)
                #Actualización de Potencias del mejor grupo NOMA
                actualizacionPotenciasc_(NBIoT.id_c, NBIoT.S[subportadora].id, Sac)


                # Actualización de Tasas del mejor grupo NOMA
                for device in range(0, NBIoT.kmax):
                    Interferencias = calculoInterferencia(subportadora, NBIoT.id_c, device)
                    R = calculoTasaTx(Interferencias, subportadora, NBIoT.id_c, device)
                    NBIoT.Cns[NBIoT.id_c].dispositivos[0][device].Rb = R


                #Validación del cumplimiento de tasas del grupo NOMA
                condicion = validacionTasas(NBIoT.id_c)
                if condicion == True:
                    # Asignación de grupo a subportadora s
                    NBIoT.Cns[NBIoT.id_c].Subcarrier = [NBIoT.S[subportadora].id]
                    NBIoT.Clusters.append(NBIoT.Cns[NBIoT.id_c])
                    # Asignación de subportadora a cluster de acuerdo con c*
                    NBIoT.S[subportadora].GrupoNOMA.append([NBIoT.id_c, NBIoT.c_])
                    #Quitar o limpiar el mejor grupo de la lista Cns
                    NBIoT.Cns[NBIoT.id_c].RTotal = 0

        NBIoT.Sv = NBIoT.Sv + 1
    #Quitar o limpiar la subportadora S' (Sv) de conjunto S

    #Validación del cumplimiento de tasas del grupo NOMA
        #For para recorrer las Subportadoras
        #Encontrar mejor grupo NOMA para cada S
        #Modificar su gamma
        #Actualizar su Sac
    #Actualizar Potencias de:
    #FIN

#Funciones que se utilizan en algoritmo de asignación de recursos

#Calcula las tasas de transmisión para un dispositivo
def calculoTasaTx(Interferencias, subportadora, cluster, device):
    return NBIoT.Cns[cluster].gamma * NBIoT.BW * mth.log2(1 + (((abs(NBIoT.Cns[cluster].dispositivos[0][device].h[subportadora]) ** 2) * (NBIoT.Cns[cluster].dispositivos[0][device].Px[subportadora])) / ((NBIoT.No * NBIoT.BW) + Interferencias)))

#Calcula la Interferencia de los dispositivos del grupo NOMA para un dispositivo
def calculoInterferencia(subportadora, cluster, device):
    Interference = 0
    #Se buscan dispositivos del mimsmo grupo pero con rangos superiores para calcular su contribución de interferencia
    for disp in range(device+1, NBIoT.kmax):
        I = (abs(NBIoT.Cns[cluster].dispositivos[0][disp].h[subportadora]) ** 2) * (NBIoT.Cns[cluster].dispositivos[0][disp].Px[subportadora])
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

def actualizacionPotenciasc_(cluster, subportadora, Sac):
    for device in range(0, NBIoT.kmax):
        NBIoT.Cns[cluster].dispositivos[0][device].Px[subportadora] = NBIoT.Cns[cluster].dispositivos[0][device].Px[subportadora] / ( Sac + 1)


def validacionTasas(cluster):
    for device in range(0, NBIoT.kmax):
        if (NBIoT.Cns[cluster].dispositivos[0][device].Rb) < (NBIoT.Cns[cluster].dispositivos[0][device].Rth):
            return False
    return True




AlgoritmoAsignacionRecursos()