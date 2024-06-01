from AnalyseBesoin.IPorte import IPorte

class PorteTest(IPorte):
    def __init__(self):
        self._ouvertures_demandees = 0
        self._fermetures_demandees = 0
        self._etat_ouverte = False

    def ouvrir(self):
        self._ouvertures_demandees += 1
        self._etat_ouverte = True

    def fermer(self):
        self._fermetures_demandees += 1
        self._etat_ouverte = False

    @property
    def ouverture_demandee(self):
        return self._etat_ouverte

    @property
    def fermeture_demandee(self):
        return not self._etat_ouverte

