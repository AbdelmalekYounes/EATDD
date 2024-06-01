from AnalyseBesoin.ILecteur import ILecteur

class LecteurTest(ILecteur):
    def __init__(self):
        self._detection_simulee = False
        self._badge_valide = True

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

    def reinitialiser_detection(self):
        self._detection_simulee = False
        self._badge_valide = True