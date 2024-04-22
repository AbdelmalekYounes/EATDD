from AnalyseBesoin.AssociationsLecteurPorte import AssociationsLecteurPorte

class MoteurOuverture:
    def __init__(self):
        self._associations = AssociationsLecteurPorte()

    def interroger(self):
        portes_a_ouvrir = set()

        # Collecter d'abord toutes les portes à ouvrir dans ce cycle
        for lecteur, portes in self._associations.associations.items():
            if lecteur.badge_detecte():
                for porte in portes:
                    portes_a_ouvrir.add(porte)

        # Ouvrir toutes les portes recueillies
        for porte in portes_a_ouvrir:
            porte.ouvrir()

    def associer(self, lecteur, porte):
        self._associations.enregistrer(lecteur, porte)
