from AnalyseBesoin.IPorte import IPorte

class PorteSpy(IPorte):
    def __init__(self):
        self._ouvertures_demandees = 0

    def ouvrir(self):
        self._ouvertures_demandees += 1

    @property
    def ouverture_demandee(self):
        return self._ouvertures_demandees > 0



