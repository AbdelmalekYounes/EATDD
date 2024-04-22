from AnalyseBesoin.IPorte import IPorte

class PorteSpy(IPorte):
    def __init__(self):
        self.ouverture_demandee = False

    def ouvrir(self):
        self.ouverture_demandee = True
