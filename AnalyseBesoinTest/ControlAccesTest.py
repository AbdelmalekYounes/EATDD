import unittest
from AnalyseBesoin.MoteurOuverture import MoteurOuverture
from .Utilities.LecteurFake import LecteurFake
from .Utilities.PorteSpy import PorteSpy

class ControleAccesTest(unittest.TestCase):

    def test_cas_nominal(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        porte = PorteSpy()
        lecteur = LecteurFake()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS le signal d'ouverture est envoyé à la porte
        self.assertTrue(porte.ouverture_demandee)

    def test_cas_aucune_interrogation(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        porte = PorteSpy()
        lecteur = LecteurFake()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(porte.ouverture_demandee)

    def test_cas_non_badge(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, n'ayant pas détecté un Badge
        porte = PorteSpy()
        lecteur = LecteurFake()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(porte.ouverture_demandee)

    def test_deux_portes(self):
        # ÉTANT DONNÉ un Lecteur ayant détecté un Badge
        # ET un autre Lecteur n'ayant rien détecté
        # ET une Porte reliée chacune à un Lecteur
        porte_devant_ouvrir = PorteSpy()
        porte_devant_rester_fermee = PorteSpy()

        lecteur_detecte = LecteurFake()
        lecteur_detecte.simuler_detection_badge()

        lecteur_non_detecte = LecteurFake()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur_detecte, porte_devant_ouvrir)
        moteur_ouverture.associer(lecteur_non_detecte, porte_devant_rester_fermee)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS seule la Porte reliée au Lecteur reçoit le signal d'ouverture
        self.assertFalse(porte_devant_rester_fermee.ouverture_demandee)
        self.assertTrue(porte_devant_ouvrir.ouverture_demandee)

    def test_deux_portes_mais_l_inverse(self):
        # Même scénario avec des paires inversées pour confirmation de la logique
        porte_devant_ouvrir = PorteSpy()
        porte_devant_rester_fermee = PorteSpy()

        lecteur_detecte = LecteurFake()
        lecteur_detecte.simuler_detection_badge()

        lecteur_non_detecte = LecteurFake()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur_non_detecte, porte_devant_rester_fermee)
        moteur_ouverture.associer(lecteur_detecte, porte_devant_ouvrir)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS seule la Porte reliée au Lecteur reçoit le signal d'ouverture
        self.assertFalse(porte_devant_rester_fermee.ouverture_demandee)
        self.assertTrue(porte_devant_ouvrir.ouverture_demandee)

if __name__ == '__main__':
    unittest.main()
