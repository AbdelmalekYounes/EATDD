# ControlAccesTest.py
import unittest
from AnalyseBesoin.MoteurOuverture import MoteurOuverture
from .Utilities.LecteurTest import LecteurTest
from .Utilities.PorteTest import PorteTest

class ControleAccesTest(unittest.TestCase):

    def test_cas_nominal(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        porte = PorteTest()
        lecteur = LecteurTest()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS le signal d'ouverture est envoyé à la porte
        self.assertTrue(porte.ouverture_demandee)

    def test_cas_aucune_interrogation(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        porte = PorteTest()
        lecteur = LecteurTest()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # QUAND le Moteur d'Ouverture n'effectue pas d'interrogation des lecteurs
        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(porte.ouverture_demandee)

    def test_cas_non_badge(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, n'ayant pas détecté un Badge
        porte = PorteTest()
        lecteur = LecteurTest()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(porte.ouverture_demandee)

    def test_cas_lecteur_non_associe(self):
        # ÉTANT DONNÉ un Lecteur non associé à une porte
        lecteur = LecteurTest()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS aucune porte ne reçoit le signal d'ouverture
        self.assertEqual(len(moteur_ouverture._portes_a_ouvrir), 0)    

    def test_deux_portes(self):
        # ÉTANT DONNÉ un Lecteur ayant détecté un Badge
        # ET un autre Lecteur n'ayant rien détecté
        # ET une Porte reliée chacune à un Lecteur
        porte_devant_ouvrir = PorteTest()
        porte_devant_rester_fermee = PorteTest()

        lecteur_detecte = LecteurTest()
        lecteur_detecte.simuler_detection_badge()

        lecteur_non_detecte = LecteurTest()

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
        porte_devant_ouvrir = PorteTest()
        porte_devant_rester_fermee = PorteTest()

        lecteur_detecte = LecteurTest()
        lecteur_detecte.simuler_detection_badge()

        lecteur_non_detecte = LecteurTest()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur_non_detecte, porte_devant_rester_fermee)
        moteur_ouverture.associer(lecteur_detecte, porte_devant_ouvrir)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS seule la Porte reliée au Lecteur reçoit le signal d'ouverture
        self.assertFalse(porte_devant_rester_fermee.ouverture_demandee)
        self.assertTrue(porte_devant_ouvrir.ouverture_demandee)

    def test_cas_2_portes(self):
        # ÉTANT DONNÉ deux Portes reliées à un Lecteur, ayant détecté un Badge
        porte1 = PorteTest()
        porte2 = PorteTest()
        lecteur = LecteurTest()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte1)
        moteur_ouverture.associer(lecteur, porte2)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS le signal d'ouverture est envoyé aux deux portes
        self.assertTrue(porte1.ouverture_demandee)
        self.assertTrue(porte2.ouverture_demandee)

    def test_cas_2_lecteurs(self):
        # ÉTANT DONNÉ une Porte reliée à deux Lecteurs, ayant tous les deux détecté un Badge
        porte = PorteTest()

        lecteur1 = LecteurTest()
        lecteur1.simuler_detection_badge()

        lecteur2 = LecteurTest()
        lecteur2.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur1, porte)
        moteur_ouverture.associer(lecteur2, porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS un seul signal d'ouverture est envoyé à la Porte
        self.assertTrue(porte.ouverture_demandee)

    def test_cas_fermeture_automatique(self):
        # ÉTANT DONNÉ une Porte ouverte, elle doit se fermer automatiquement après une période d'inactivité
        porte = PorteTest()
        lecteur = LecteurTest()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS la porte se ferme automatiquement après une période d'inactivité
        self.assertTrue(porte.ouverture_demandee)
        moteur_ouverture.attendre(2)  # Utilisation de 2 secondes pour simuler l'inactivité
        self.assertFalse(porte.ouverture_demandee)  # La porte ne doit plus être ouverte
        self.assertTrue(porte.fermeture_demandee)  # La porte doit être fermée

    def test_cas_duree_ouverte(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        porte = PorteTest()
        lecteur = LecteurTest()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()
        moteur_ouverture.associer(lecteur, porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS la porte reste ouverte pendant une durée prédéfinie
        self.assertTrue(porte.ouverture_demandee)
        moteur_ouverture.attendre(3)  # Utilisation de 3 secondes pour vérifier que la porte reste ouverte
        self.assertFalse(porte.ouverture_demandee)  # La porte doit se fermer après la durée prédéfinie

    def test_cas_lecteur_non_associe(self):
        # ÉTANT DONNÉ un Lecteur non associé à une porte
        lecteur = LecteurTest()
        lecteur.simuler_detection_badge()

        moteur_ouverture = MoteurOuverture()

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        moteur_ouverture.interroger()

        # ALORS aucune porte ne reçoit le signal d'ouverture
        self.assertEqual(len(moteur_ouverture._portes_a_ouvrir), 0)


if __name__ == '__main__':
    unittest.main()
