class Simulacion(object):
    def __init__(self, umbralArribos, PLE, r_cell, Ciclos):
        self.umbralArribos = umbralArribos          #Umbral de arribos para paro de la simulación
        self.PLE = PLE       #Path Loss Exponent
        self.r_cell = r_cell #Radio de la celula
        self.Ciclos = Ciclos #Ciclos que toma el algoritmo de aisgnacion de recursos para acabar de asignar subportadoras