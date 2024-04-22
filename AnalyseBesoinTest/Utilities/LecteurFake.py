from AnalyseBesoin.ILecteur import ILecteur

class LecteurFake(ILecteur):
    def __init__(self):
        self._detection_simulee = False

    def badge_detecte(self):
        returned_value = self._detection_simulee
        self._detection_simulee = False
        return returned_value

    def simuler_detection_badge(self):
        self._detection_simulee = True
