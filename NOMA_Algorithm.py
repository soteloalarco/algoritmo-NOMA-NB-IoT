import math as mth
import copy
from Clases.GrupoNOMA import  GrupoNOMA
from Clases.Subportadora import Subportadora
from Clases.NB_IoT import NB_IoT
from Funciones.FuncionDispositivo import creardispositivos
from Clases.Simulacion import Simulacion

#Creación de Objetos para la simulación
DESsim = Simulacion(0, 3, 500)
NBIoT = NB_IoT(48, [], [], [], [], 48, [], 49, [], 200, [], 0, [], 4, 3.75e3, 5.012e-21)

#Creacion de Dispositivos URLLC
NBIoT.U.append(creardispositivos(NBIoT.numU, 1, DESsim.PLE, DESsim.r_cell, NBIoT.numS))
#Creacion de Dispositivos mMTC
NBIoT.M.append(creardispositivos(NBIoT.numM, 2, DESsim.PLE, DESsim.r_cell, NBIoT.numS))


def AlgoritmoAgrupacionNOMA():
    # Se empiezan a agrupar usuarios con una alta ganancia de canal promedio,
    # en la recepción tipo SIC se decodifican primero los usuarios con una alta ganancia de canal promedio antes que los de baja ganancia  de canal promedio
    # Los rangos de los dispositivos uRLLC deben ser menores que los MTC para que sea eficiente la decodificación SIC

    # indices que indican cual es la última posición de asignación de usuarios URLLC
    indicePos1Grupo = 0
    indicePos2Grupo = 0

    # AGRUPAMIENTO DE USUARIOS URLLC
    # Solo para grupos de 4 usuarios
    for deviceURLLC in range(0, int(NBIoT.numU)):
        # deviceURLLC corresponde al número de dispositivos uRLLC [U]
        if deviceURLLC < NBIoT.numC:
            # Asignar los dispositivos uRLLC a rangos bajos de los primeros grupos
            NBIoT.C.append(GrupoNOMA(deviceURLLC, [], False, 0, 0, 0, 1, [], []))
            NBIoT.C[deviceURLLC].dispositivos.append([NBIoT.U[0][deviceURLLC], False, False, False, False])
            NBIoT.U[0][deviceURLLC].alphabeta = 1
            indicePos1Grupo = indicePos1Grupo + 1

        #Validación de que si el agrupamiento es de 2 entonces solo se asignarán al rango 1
        elif deviceURLLC < 2*NBIoT.numC:
            # Si el número de dispositivos uRLLC [U] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
            # serán asignados a los siguientes rangos del grupo
            NBIoT.C[indicePos2Grupo].dispositivos[0][1] = NBIoT.U[0][deviceURLLC]
            NBIoT.U[0][deviceURLLC].alphabeta = 1
            indicePos2Grupo = indicePos2Grupo + 1
        else:
            #Solo se podrán asignar dispositivos URLLC hasta el segundo rango  de cada cluster
            print('Se asignaron',deviceURLLC, 'usuarios URLLC pero eran ', NBIoT.numU, ' usuarios MTC' )
            break


    #Se checa en que cluster se quedó asignado el ultimo dispositivo URLLC
    if indicePos2Grupo != 0:
        indiceAsignacionCluster = indicePos2Grupo
        cerosEliminar = indicePos2Grupo
        # k _= es una variable que indica en que rango se quedó asignado el ultimo dispositivo URLLC
        k_= 1
        if indicePos2Grupo == NBIoT.numS:
           indiceAsignacionCluster = 0
           cerosEliminar=0
           k_ = 2
    else:
        indiceAsignacionCluster = indicePos1Grupo
        cerosEliminar = indicePos1Grupo
        k_=0

        if indiceAsignacionCluster != 48:
            for cn in range(indiceAsignacionCluster, int(NBIoT.numC)):
                NBIoT.C.append(GrupoNOMA(cn, [], False, 0, 0, 0, 1, [], []))
                NBIoT.C[cn].dispositivos.append([False, False, False, False, False])
        else:
            indiceAsignacionCluster =0
            cerosEliminar=0
            k_ = 1


    # Agregar ceros a lista de usuarios MTC para que se empiezen a agrupar desde esa posición
    for g in range(0, indiceAsignacionCluster):
        NBIoT.M[0].insert(0, 0)

    # AGRUPAMIENTO DE USUARIOS mMTC
    for deviceMTC in range(indiceAsignacionCluster, len(NBIoT.M[0])):
        # Si el número de dispositivos mMTC [M] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
        # serán asignados a los siguientes rangos del grupo, última posición de asignación

        # Asignar los dispositivos mmtc a los rangos mas bajos de los primeros grupos
        NBIoT.C[indiceAsignacionCluster].dispositivos[0][k_] = NBIoT.M[0][deviceMTC]
        NBIoT.M[0][deviceMTC].alphabeta = 1
        indiceAsignacionCluster = indiceAsignacionCluster + 1

        if indiceAsignacionCluster == (NBIoT.numS):
            k_ = k_ + 1
            indiceAsignacionCluster = 0
            if k_ == NBIoT.kmax:
                print('Se asignaron',deviceMTC, 'usuarios MTC pero eran ', NBIoT.numM, ' usuarios MTC' )
                break

    # Eliminar ceros que se agregaron a lista
    del NBIoT.M[0][0:cerosEliminar]


#Ejecución del algoritmo para la agrupación NOMA
AlgoritmoAgrupacionNOMA()




#  *******************************************  Algoritmo para la asignación de recursos NOMA (subportadoras) **********************************************
def AlgoritmoAsignacionRecursos():
    NBIoT.Sv = 0
    # Conjunto de clusters de dispositivos con tasas insatisfechas
    #NBIoT.Cns = copy.deepcopy(NBIoT.C)
    #Creacion de Subportadoras NB_IoT cada una con 48 grupos NOMA
    for s in range(0, NBIoT.numS):
        CLUSTER = copy.deepcopy(NBIoT.C)
        NBIoT.S.append(Subportadora(s, CLUSTER, 0, []))

    #Inicio del bucle del algoritmo de asignación de recursos
    while True:
        if (len(NBIoT.Agrupaciones) == NBIoT.numS):
            break

        # For para recorrer las 48 subportadoras
        for subportadora in range(0, NBIoT.numS):
            if NBIoT.S[subportadora].Cluster == []:
                NBIoT.S[subportadora].c_ = False
                # For para recorrer los grupos no asignados de Cns
                for cluster in range(0, NBIoT.numC):
                    #Validación de que el cluster ya esté asignado a una subportadora
                    NBIoT.S[subportadora].C[cluster].RTotal = 0
                    if NBIoT.S[subportadora].C[cluster].Subcarrier == []:
                        #NBIoT.S[subportadora].C[cluster].Sac = []
                        #NBIoT.S[subportadora].C[cluster].Px = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
                        # For para recorrer los rangos del grupo
                        for device in range(0, NBIoT.kmax):
                            #Validación de que algun rango del cluster está vacio o desocupado
                            if NBIoT.S[subportadora].C[cluster].dispositivos[0][device] != False:
                                Interferencias = calculoInterferencia(subportadora, cluster, device)
                                R = calculoTasaTx(Interferencias, subportadora, cluster, device)
                                # Se asigna la tasa lograda a dispositivo URLLC
                                NBIoT.S[subportadora].C[cluster].dispositivos[0][device].Rx = R
                                NBIoT.S[subportadora].C[cluster].RTotal = NBIoT.S[subportadora].C[cluster].RTotal + R

                #Grupo NOMA que maximiza la tasa
                NBIoT.S[subportadora].c_ = busquedaMejorGrupoNOMA(subportadora)
                if NBIoT.S[subportadora].c_ == 49:
                    return 0

                #Actualizar lista de subportadoras asignadas al cluster Sac
                NBIoT.S[subportadora].C[NBIoT.S[subportadora].c_].Sac.append(NBIoT.S[subportadora].id)
                Sac = len(NBIoT.S[subportadora].C[NBIoT.S[subportadora].c_].Sac)

                #Actualización de Potencias del mejor grupo NOMA
                actualizacionPotenciasc_(NBIoT.S[subportadora].c_, NBIoT.S[subportadora].id, Sac)

                # Actualización de Tasas del mejor grupo NOMA
                for device in range(0, NBIoT.kmax):
                    # Validación de que algun rango del cluster está vacio o desocupado
                    if NBIoT.S[subportadora].C[NBIoT.S[subportadora].c_].dispositivos[0][device] != False:
                        Interferencias = calculoInterferencia(subportadora, NBIoT.S[subportadora].c_, device)
                        R = calculoTasaTx(Interferencias, subportadora, NBIoT.S[subportadora].c_, device)
                        NBIoT.S[subportadora].C[NBIoT.S[subportadora].c_].dispositivos[0][device].Rx = R

                # Validación del cumplimiento de tasas del mejor grupo NOMA c_ (c*)
                condicion = validacionTasas(subportadora, NBIoT.S[subportadora].c_)

                # Retribución de subportadora a cluster de acuerdo con c* en caso de que se cumplan los umbrales de las tasas
                if condicion == True:
                    # Asignación de subportadora s a grupos NOMA
                    for sb in range(0, NBIoT.numS):
                        NBIoT.S[sb].C[NBIoT.S[subportadora].c_].Subcarrier = [NBIoT.S[subportadora].id]
                    # Asignación de grupo NOMA a subportadora s
                    NBIoT.S[subportadora].Cluster = [NBIoT.S[subportadora].c_]
                    #Asignacion de s y c por medio de sus ids en lista Agrupaciones
                    NBIoT.Agrupaciones.append([NBIoT.S[subportadora].id, NBIoT.S[subportadora].c_])


#Funciones que se utilizan en algoritmo de asignación de recursos

#Calcula las tasas de transmisión para un dispositivo
def calculoTasaTx(Interferencias, subportadora, cluster, device):
    return NBIoT.BW * mth.log2(1 + (((abs(NBIoT.S[subportadora].C[cluster].dispositivos[0][device].h[subportadora]) ** 2) * (NBIoT.S[subportadora].C[cluster].dispositivos[0][device].Px[subportadora])) / ((NBIoT.No * NBIoT.BW) + Interferencias)))

#Calcula la Interferencia de los dispositivos del grupo NOMA para un dispositivo
def calculoInterferencia(subportadora, cluster, device):
    Interference = 0
    #Se buscan dispositivos del mimsmo grupo pero con rangos superiores para calcular su contribución de interferencia
    for disp in range(device+1, NBIoT.kmax):
        # Validación de que algun rango del cluster está vacio o desocupado
        if NBIoT.S[subportadora].C[cluster].dispositivos[0][disp] != False :
            I = (abs(NBIoT.S[subportadora].C[cluster].dispositivos[0][disp].h[subportadora]) ** 2) * (NBIoT.S[subportadora].C[cluster].dispositivos[0][disp].Px[subportadora])
            Interference = Interference + I
    return Interference

#La optimización del algoritmo es de acuerdo con el grupo NOMA que maximize la tasa de transmisión
def busquedaMejorGrupoNOMA(subportadora):
    # Se busca el grupo que mejor maximize la tasa de acuerdo con Rtotal
    buscargrupo = max(GrupoNOMA.RTotal for GrupoNOMA in NBIoT.S[subportadora].C)
    if buscargrupo==0:
        return 49
    for cluster in range(0, NBIoT.numC):
        #Se busca el identificador del mejor grupo
        if NBIoT.S[subportadora].C[cluster].RTotal == buscargrupo:
            break
    #Asignación de c*
    #NBIoT.c_ = NBIoT.Cns[cluster]
    return NBIoT.S[subportadora].C[cluster].id

def actualizacionPotenciasc_(cluster, subportadora, Sac):
    for device in range(0, NBIoT.kmax):
        # Validación de que algun rango del cluster está vacio o desocupado
        if NBIoT.S[subportadora].C[cluster].dispositivos[0][device] != False:
            NBIoT.S[subportadora].C[cluster].dispositivos[0][device].Px[subportadora] = (NBIoT.S[subportadora].C[cluster].dispositivos[0][device].Px[subportadora] / (Sac + 1))


def validacionTasas(subportadora, cluster):
    for device in range(0, NBIoT.kmax):
        # Validación de que algun rango del cluster está vacio o desocupado
        if NBIoT.S[subportadora].C[cluster].dispositivos[0][device] != False:
            if (NBIoT.S[subportadora].C[cluster].dispositivos[0][device].Rx) < (NBIoT.S[subportadora].C[cluster].dispositivos[0][device].Rth):
                return False
    return True

ParoFcn = 0
ParoFcn = AlgoritmoAsignacionRecursos()
NBIoT.Agrupaciones.sort()