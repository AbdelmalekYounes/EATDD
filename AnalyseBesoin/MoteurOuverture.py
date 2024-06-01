import time
from AnalyseBesoin.AssociationsLecteurPorte import AssociationsLecteurPorte

class MoteurOuverture:
    def __init__(self):
        self._associations = AssociationsLecteurPorte()
        self._portes_a_ouvrir = set()

    def interroger(self):

        # Collecter d'abord toutes les portes à ouvrir dans ce cycle
        for lecteur, portes in self._associations.associations.items():
            if lecteur.badge_detecte():
                for porte in portes:
                    self._portes_a_ouvrir.add(porte)

        # Ouvrir toutes les portes recueillies
        for porte in self._portes_a_ouvrir:
            porte.ouvrir()

    def associer(self, lecteur, porte):
        self._associations.enregistrer(lecteur, porte)

    def attendre(self, duree):
         # Attendre une certaine durée en secondes
        time.sleep(duree)
        # Fermer les portes après la période d'attente
        for porte in self._portes_a_ouvrir:
            porte.fermer()
        self._portes_a_ouvrir.clear()