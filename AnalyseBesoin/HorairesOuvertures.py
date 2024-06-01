from datetime import time, datetime

class HorairesOuvertures:
    def __init__(self, heure_debut: time, heure_fin: time):
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin

    def est_dans_horaire(self) -> bool:
        date_du_jour = datetime.now()
        heure_actuelle = date_du_jour.time()
        return self.heure_debut <= heure_actuelle <= self.heure_fin