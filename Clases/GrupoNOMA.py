class GrupoNOMA(object):
    def __init__(self, id, dispositivos, tasasSatisfechas, Ru, Rm, RTotal, gamma, Sac, Subcarrier):
        self.id = id        # Identificador de Grupo
        self.dispositivos = dispositivos    #Lista de dispositivos agrupados en orden
        self.tasasSatisfechas = tasasSatisfechas        #Variable booleana que indica si las tasas de los dispositivos está
        self.Ru = Ru                #Tasa de transmisión de dispositivos URLLC acumulada por grupo
        self.Rm = Rm                #Tasa de transmisión de dispositivos MTC acumulada por grupo
        self.RTotal = RTotal        #RTotal acumula las tasas de cada dispositivo por grupo y asi obtener la tasa alcanzada por grupo
        self.gamma = gamma          #Variable binaria que indica la asignación de un cluster para una subportadora
        self.Sac = Sac              #Conjunto de subportadoras asignadas a un cluster C
        self. Subcarrier = Subcarrier   #Subportadora asignada a cluster
