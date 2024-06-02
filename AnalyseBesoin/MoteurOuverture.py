from datetime import time
import time as TimeSleep
from .AssociationsLecteurPorte import AssociationsLecteurPorte
from .HorairesOuvertures import HorairesOuvertures

class MoteurOuverture:
    def __init__(self, heure_debut=None, heure_fin=None):
        self._associations = AssociationsLecteurPorte()
        self._portes_a_ouvrir = set()
        self._heure_debut = heure_debut
        self._heure_fin = heure_fin

    def interroger(self, heure_actuelle=None):
        portes_a_ouvrir = set()
        for lecteur, portes in self._associations.associations.items():
            if lecteur.badge_detecte():
                if lecteur.est_admin() or (heure_actuelle is None or self._heure_debut <= heure_actuelle <= self._heure_fin):
                    for porte in portes:
                        portes_a_ouvrir.add(porte)

        for porte in portes_a_ouvrir:
            porte.ouvrir()
        self._portes_a_ouvrir = portes_a_ouvrir

    def associer(self, lecteur, porte):
        self._associations.enregistrer(lecteur, porte)

    def desactiver(self, porte):
        for lecteurs in self._associations.associations.values():
            if porte in lecteurs:
                lecteurs.remove(porte)

    def attendre(self, duree):
        import time
        time.sleep(duree)
        for porte in self._portes_a_ouvrir:
            porte.fermer()
        self._portes_a_ouvrir.clear()