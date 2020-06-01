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
