import math as mth
import copy
from Clases.GrupoNOMA import GrupoNOMA
from Clases.Subportadora import Subportadora
from Clases.NB_IoT import NB_IoT
from Funciones.FuncionDispositivo import creardispositivos
from Clases.Simulacion import Simulacion

# Variables de entrada
RadioCelular = 500
PLE = 3
NumDispositivosURLLC = 48
NumDispositivosMTC = 100
kmax = 4
Numero_clusters = 48

#Creación de Objetos para la simulación
DESsim = Simulacion(0, PLE, RadioCelular, 0)
NBIoT = NB_IoT(48, [], [], [], [], Numero_clusters, [], NumDispositivosURLLC, [], NumDispositivosMTC, [], 0, [], kmax, 3.75e3, 5.012e-21)
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
            NBIoT.C[deviceURLLC].dispositivos.append([NBIoT.U[0][deviceURLLC], False, False, False, False, False])
            NBIoT.U[0][deviceURLLC].alphabeta = 1
            indicePos1Grupo = indicePos1Grupo + 1
            if (indicePos1Grupo == NBIoT.numC) and (NBIoT.kmax == 1):
                return 0

        #Validación de que si el agrupamiento es de 2 entonces solo se asignarán al rango 1
        elif deviceURLLC < 2*NBIoT.numC:
            # Si el número de dispositivos uRLLC [U] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
            # serán asignados a los siguientes rangos del grupo
            NBIoT.C[indicePos2Grupo].dispositivos[0][1] = NBIoT.U[0][deviceURLLC]
            NBIoT.U[0][deviceURLLC].alphabeta = 1
            indicePos2Grupo = indicePos2Grupo + 1

            if (indicePos2Grupo == NBIoT.numC) and (NBIoT.kmax == 2):
                return 0
        else:
            #Solo se podrán asignar dispositivos URLLC hasta el segundo rango  de cada cluster
            #print('Se asignaron',deviceURLLC, 'usuarios URLLC pero eran ', NBIoT.numU, ' usuarios MTC' )
            break


    #Se checa en que cluster se quedó asignado el ultimo dispositivo URLLC
    if indicePos2Grupo != 0:
        indiceAsignacionCluster = indicePos2Grupo
        cerosEliminar = indicePos2Grupo
        # k _= es una variable que indica en que rango se quedó asignado el ultimo dispositivo URLLC
        k_= 1
        if indicePos2Grupo == NBIoT.numC:####
           indiceAsignacionCluster = 0
           cerosEliminar=0
           k_ = 2
    else:
        indiceAsignacionCluster = indicePos1Grupo
        cerosEliminar = indicePos1Grupo
        k_=0

        if indiceAsignacionCluster != NBIoT.numC:######
            #TODO implementar esto para un numero de clusters variable no fijo
            for cn in range(indiceAsignacionCluster, int(NBIoT.numC)):
                NBIoT.C.append(GrupoNOMA(cn, [], False, 0, 0, 0, 1, [], []))
                NBIoT.C[cn].dispositivos.append([False, False, False, False, False, False])
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

        if indiceAsignacionCluster == (NBIoT.numC):######
            k_ = k_ + 1
            indiceAsignacionCluster = 0
            if k_ == NBIoT.kmax:
                #print('Se asignaron',deviceMTC, 'usuarios MTC pero eran ', NBIoT.numM, ' usuarios MTC' )
                break

    # Eliminar ceros que se agregaron a lista
    del NBIoT.M[0][0:cerosEliminar]

#Ejecución del algoritmo para la agrupación NOMA
AlgoritmoAgrupacionNOMA()



#  *******************************************  Algoritmo para la asignación de recursos NOMA (subportadoras) **********************************************
#TODO implementar meno cluter que 48
def AlgoritmoAsignacionRecursos():

    #Conjunto de clusters de dispositivos con tasas insatisfechas
    NBIoT.Cns = copy.deepcopy(NBIoT.C)

    #Creacion de Subportadoras NB_IoT cada una con 48 grupos NOMA
    for s in range(0, NBIoT.numS):
        NBIoT.S.append(Subportadora(s, [], 0, []))

    DESsim.Ciclos = 0

    #Inicio del bucle del algoritmo de asignación de recursos
    #while True:
    #    # TODO checar eta condicón y cambiarla por una en la que se acaben las subportadores
    #    if (NBIoT.S == []):
    #        break


    DESsim.Ciclos = DESsim.Ciclos + 1

    NBIoT.numS = len(NBIoT.S)

    # For para recorrer todas las subportadoras disponibles
    for subportadora in range(0, NBIoT.numS):
        NBIoT.S[subportadora].c_ = []
        NBIoT.Sv = []
        NBIoT.numC = len(NBIoT.Cns)
        # For para recorrer los grupos NOMA no satisfechos (Cns)
        # TODO Cambiar la condición a una como en el algoritmo, que c este en Cns
        for cluster in range(0, NBIoT.numC):
            #Inicilalización a cero de las tasas totales de cada cluster
            NBIoT.Cns[cluster].RTotal = 0
            # For para recorrer todos los rangos del grupo NOMA
            for device in range(0, NBIoT.kmax):
                #Validación de que algun rango del cluster está vacio o desocupado
                if NBIoT.Cns[cluster].dispositivos[0][device] != False:
                    Interferencias = calculoInterferencia(NBIoT.Cns, subportadora, cluster, device)
                    R = calculoTasaTx(Interferencias, NBIoT.Cns, subportadora, cluster, device)
                    # Se asigna la tasa lograda a dispositivo
                    NBIoT.Cns[cluster].dispositivos[0][device].Rx = R
                    NBIoT.Cns[cluster].RTotal = NBIoT.Cns[cluster].RTotal + R

        #Grupo NOMA que maximiza la tasa
        NBIoT.S[subportadora].c_ = busquedaMejorGrupoNOMA(NBIoT.Cns)

        #Se busca en la lista Cns el grupo NOMA que maximiza la tasa
        ID_cluster_c = busquedaIDCns(NBIoT.Cns, NBIoT.S[subportadora].c_)

        #Actualizar lista de subportadoras asignadas al cluster Sac
        NBIoT.Cns[ID_cluster_c].Sac.append(NBIoT.S[subportadora].id)

        Sac = len(NBIoT.Cns[ID_cluster_c].Sac)

        # TODO implementar la S^ para tener regitro de las s que quedan
        NBIoT.Sv.append(NBIoT.S[subportadora].id)

        #TODO Actualizar las tasas des dispositivos en el cluter c* que gano la subportadora
        #NO COINCIDO EN ESTE "TO DO", YO ACTUALIZO LAS TASAS UNA VEZ QUE SUS POTENCIAS SE HAYAN ACTUALIZADO

        #Actualización de Potencias del mejor grupo NOMA
        NBIoT.Cns = actualizacionPotenciasc_(NBIoT.Cns,ID_cluster_c, NBIoT.S[subportadora].id, Sac)

        # Actualización de Tasas del mejor grupo NOMA
        for device in range(0, NBIoT.kmax):
            # Validación de que algun rango del cluster está vacio o desocupado
            if NBIoT.Cns[ID_cluster_c].dispositivos[0][device] != False:
                Interferencias = calculoInterferencia(NBIoT.Cns ,subportadora, ID_cluster_c, device)
                R = calculoTasaTx(Interferencias, NBIoT.Cns, subportadora, ID_cluster_c, device)
                NBIoT.Cns[ID_cluster_c].dispositivos[0][device].Rx = R

        NBIoT.Cns = actualizacionTasasc_(NBIoT.Cns, ID_cluster_c)

        # Validación del cumplimiento de tasas del mejor grupo NOMA c_ (c*)
        condicion = validacionTasas(NBIoT.Cns, ID_cluster_c)

        # Retribución de subportadora a cluster de acuerdo con c* en caso de que se cumplan los umbrales de las tasas
        if condicion == True:
            # Asignación de subportadora s a grupo NOMA
            #TODO es esto equivalente a actualizar Sca ? en el algoritmo agregramo el cluster a lo que cumplen su tasa
            #Aqui asignar a los Sac*********

            #Asignacion de s y c por medio de sus ids en lista Agrupaciones
            NBIoT.Agrupaciones.append([NBIoT.S[subportadora], NBIoT.Cns[ID_cluster_c]])

            NBIoT.Cns[ID_cluster_c] = 0
            #TODO quitar a  c_ de los cluters que no han cumplido su tasa Cns
            #Limpiar Lista de Cns ya asignadas
            for clus in range(0, len(NBIoT.Cns)):
                if NBIoT.Cns[clus] == 0:
                    del NBIoT.Cns[clus]
                    break

        #TODO agregar  s a S^ o de alguna manera limitar que esa ssubportadora ya no se encuentra disponible
        #Buscar cual fue la subportadora que se asignó

        NBIoT.S[subportadora] = 0

    #Limpiar Lista de Subportadoras ya asignadas
    sub = 0
    numS = len(NBIoT.S)
    while sub < numS:
        if NBIoT.S[sub] == 0:
            del NBIoT.S[sub]
            numS -= 1
        else:
            sub += 1

    #TODO Tal vez implementar la segunda parte, donde se asignan las subportadoras sobrantes
    #Validación de todas las tasas de los usuarios



#Funciones que se utilizan en algoritmo de asignación de recursos

#Calcula la Interferencia de los dispositivos del grupo NOMA para un dispositivo
def calculoInterferencia(ListaClusters, subportadora, cluster, device):
    Interference = 0
    #Se buscan dispositivos del mimsmo grupo pero con rangos superiores para calcular su contribución de interferencia
    for disp in range(device+1, NBIoT.kmax):
        # Validación de que algun rango del cluster está vacio o desocupado
        if ListaClusters[cluster].dispositivos[0][disp] != False:
            I = (abs(ListaClusters[cluster].dispositivos[0][disp].h[subportadora]) ** 2) * (ListaClusters[cluster].dispositivos[0][disp].Px[subportadora])
            Interference = Interference + I
    return Interference

#Calcula las tasas de transmisión para un dispositivo
def calculoTasaTx(Interferencias, ListaClusters,  subportadora, cluster, device):
    return NBIoT.BW * mth.log2(1 + (((abs(ListaClusters[cluster].dispositivos[0][device].h[subportadora]) ** 2) * (ListaClusters[cluster].dispositivos[0][device].Px[subportadora])) / ((NBIoT.No * NBIoT.BW) + Interferencias)))

# La optimización del algoritmo es de acuerdo con el grupo NOMA que maximize la tasa de transmisión
# Esta función busca el mejor grupo NOMA, es decir, el que maximize la tasa con base en las tasas que logra cada cluster (Rtotal)
def busquedaMejorGrupoNOMA(ListaClusters):
    buscargrupo = max(GrupoNOMA.RTotal for GrupoNOMA in ListaClusters)
    for cluster in range(0, NBIoT.numC):
        #Se busca el identificador del mejor grupo
        if ListaClusters[cluster].RTotal == buscargrupo:
            break
    return ListaClusters[cluster].id

#Como la lista Cns es dinámica los indices van a ir cambiendo por lo que el id no correspondrá con el indice por eso se busca su id
def busquedaIDCns(ListaClusters, ID):
    for cluster in range(0, len(ListaClusters)):
        #Se busca el identificador del cluster
        if ListaClusters[cluster].id == ID:
            break
    return cluster

#Como la lista S es dinámica los indices van a ir cambiendo por lo que el id no correspondrá con el indice por eso se busca su id
def busquedaIDSub(ListaSubportadoras, ID):
    for subportadora in range(0, len(ListaSubportadoras)):
        # Se busca el identificador de la subportadora
        if ListaSubportadoras[subportadora].id == ID:
            break
    return subportadora

#Se actualizan las tasas de los dispositivos de acuerdo
def actualizacionTasasc_(ListaClusters, cluster):
    for device in range(0, NBIoT.kmax):
        # Validación de que algun rango del cluster está vacio o desocupado
        if ListaClusters[cluster].dispositivos[0][device] != False:
            # Rx va ir cambiando en cada dispositivo entonces por eso se crea un nuevo campo Rs que indica la suma acumulada por subportadora
            ListaClusters[cluster].dispositivos[0][device].Rs = ListaClusters[cluster].dispositivos[0][device].Rs + ListaClusters[cluster].dispositivos[0][device].Rx
    return ListaClusters

#Función que actualiza las potencias de los dispositivos de un determinado cluster de acuerdo con Sac
def actualizacionPotenciasc_(ListaClusters, cluster, subportadora, Sac):
    for device in range(0, NBIoT.kmax):
        # Validación de que algun rango del cluster está vacio o desocupado
        if ListaClusters[cluster].dispositivos[0][device] != False:
            ListaClusters[cluster].dispositivos[0][device].Px[subportadora] = ListaClusters[cluster].dispositivos[0][device].Px[subportadora] / ( Sac + 1)
    return ListaClusters

#Función que checa que las tasas de los dispositivos sean satisfacidas
def validacionTasas(ListaClusters, cluster):
    for device in range(0, NBIoT.kmax):
        # Validación de que algun rango del cluster está vacio o desocupado
        if ListaClusters[cluster].dispositivos[0][device] != False:
            if (ListaClusters[cluster].dispositivos[0][device].Rs) < (ListaClusters[cluster].dispositivos[0][device].Rth):
                return False
    return True

AlgoritmoAsignacionRecursos()
#NBIoT.Agrupaciones.sort()