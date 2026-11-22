class no:

    def __init__(self, id, adj):
        self.id = id
        self.cor = None
        self.adj = adj
        self.pai = None
        self.dis = None

        self.inicio = None
        self.fim = None


    def getAdj(self):
        return self.adj
    def getId(self):
        return self.id
    def getPai(self):
        return self.pai
    def getDis(self):
        return self.dis
    def getCor(self):
        return self.cor
    def getInicio(self):
        return self.inicio
    def getFim(self):
        return self.fim

    def setPai(self, no):
        self.pai = no
    def setDis(self, distancia):
        self.dis = distancia
    def setCor(self, cor):
        self.cor = cor

    def setInicio(self, inicio):
        self.inicio = inicio

    def setFim(self, fim):
        self.fim = fim

    
        