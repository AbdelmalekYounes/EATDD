from AnalyseBesoin.ILecteur import ILecteur

class LecteurTest(ILecteur):
    def __init__(self):
        self._detection_simulee = False
        self._badge_valide = True
        self._is_admin = False
        self._horaire_autorise_debut = None
        self._horaire_autorise_fin = None

    def badge_detecte(self):
        if self._detection_simulee:
            detection = self._badge_valide
            self._detection_simulee = False
            return detection
        return False

    def simuler_detection_badge(self):
        self._detection_simulee = True
        self._badge_valide = True

    def simuler_detection_badge_invalide(self):
        self._detection_simulee = True
        self._badge_valide = False

    def rendre_admin(self):
        self._is_admin = True

    def definir_contraintes_horaires(self, debut, fin):
        self._horaire_autorise_debut = debut
        self._horaire_autorise_fin = fin

    def est_admin(self):
        return self._is_admin

    def est_autorise_heure(self, heure_actuelle):
        if self._horaire_autorise_debut and self._horaire_autorise_fin:
            return self._horaire_autorise_debut <= heure_actuelle <= self._horaire_autorise_fin
        return True