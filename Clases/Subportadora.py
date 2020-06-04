import numpy as np
import math as mth
import random
import operator
import copy

class Subportadora(object):
    def __init__(self, id,  GrupoNOMA):
        self.id = id                #Identificador para cada suubportadora
        #self.idGrupo = idGrupo      #Identificador grupo NOMA
        self.GrupoNOMA = GrupoNOMA  #Grupo NOMA


