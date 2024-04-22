class MoteurOuverture:
    def __init__(self):
        self._associations = {}

    def interroger(self):
        for lecteur, porte in self._associations.items():
            if lecteur.badge_detecte():
                porte.ouvrir()

    def associer(self, lecteur, porte):
        self._associations[lecteur] = porte
