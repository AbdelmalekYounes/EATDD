from datetime import time
import time as TimeSleep
from .AssociationsLecteurPorte import AssociationsLecteurPorte
from .HorairesOuvertures import HorairesOuvertures

class MoteurOuverture:
    def __init__(self, heure_debut: time, heure_fin: time):
        self._associations = AssociationsLecteurPorte()
        self._portes_a_ouvrir = set()
        self.horaires_ouvertures = HorairesOuvertures(heure_debut, heure_fin)

    def interroger(self, horaires_validations: bool = False):
        if self.horaires_ouvertures.est_dans_horaire() or horaires_validations == False:
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
        TimeSleep.sleep(duree)
        # Fermer les portes après la période d'attente
        for porte in self._portes_a_ouvrir:
            porte.fermer()
        self._portes_a_ouvrir.clear()

    def desactiver(self, porte):
        # Désactiver une porte spécifique
        for lecteurs in self._associations.associations.values():
            if porte in lecteurs:
                lecteurs.remove(porte)    