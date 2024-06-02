# ControlAccesTest.py
from datetime import datetime, time
import unittest
from AnalyseBesoin.AssociationsLecteurPorte import AssociationsLecteurPorte
from AnalyseBesoin.MoteurOuverture import MoteurOuverture
from .Utilities.LecteurTest import LecteurTest
from .Utilities.PorteTest import PorteTest

class ControleAccesTest(unittest.TestCase):

    def setUp(self):
        self.heure_debut = time(9)
        self.heure_fin = time(18)

        self.heure_actuelle = datetime.now().time()

        self.lecteur = LecteurTest()
        self.porte = PorteTest()
        self.moteur = MoteurOuverture(self.heure_debut, self.heure_fin)

    def test_cas_nominal(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS le signal d'ouverture est envoyé à la porte
        self.assertTrue(self.porte.ouverture_demandee)

    def test_cas_aucune_interrogation(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture n'effectue pas d'interrogation des lecteurs
        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(self.porte.ouverture_demandee)

    def test_cas_non_badge(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, n'ayant pas détecté un Badge

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(self.porte.ouverture_demandee)

    def test_cas_lecteur_non_associe(self):
        # ÉTANT DONNÉ un Lecteur non associé à une porte
        lecteur = LecteurTest()
        self.lecteur.simuler_detection_badge()


        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS aucune porte ne reçoit le signal d'ouverture
        self.assertEqual(len(self.moteur._portes_a_ouvrir), 0)    

    def test_deux_portes(self):
        # ÉTANT DONNÉ un Lecteur ayant détecté un Badge
        # ET un autre Lecteur n'ayant rien détecté
        # ET une Porte reliée chacune à un Lecteur
        porte_devant_ouvrir = PorteTest()
        porte_devant_rester_fermee = PorteTest()

        lecteur_detecte = LecteurTest()
        lecteur_detecte.simuler_detection_badge()

        lecteur_non_detecte = LecteurTest()

        self.moteur.associer(lecteur_detecte, porte_devant_ouvrir)
        self.moteur.associer(lecteur_non_detecte, porte_devant_rester_fermee)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

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

        self.moteur.associer(lecteur_non_detecte, porte_devant_rester_fermee)
        self.moteur.associer(lecteur_detecte, porte_devant_ouvrir)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS seule la Porte reliée au Lecteur reçoit le signal d'ouverture
        self.assertFalse(porte_devant_rester_fermee.ouverture_demandee)
        self.assertTrue(porte_devant_ouvrir.ouverture_demandee)

    def test_cas_2_portes(self):
        # ÉTANT DONNÉ deux Portes reliées à un Lecteur, ayant détecté un Badge
        porte1 = self.porte
        porte2 = self.porte
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, porte1)
        self.moteur.associer(self.lecteur, porte2)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS le signal d'ouverture est envoyé aux deux portes
        self.assertTrue(porte1.ouverture_demandee)
        self.assertTrue(porte2.ouverture_demandee)

    def test_cas_2_lecteurs(self):
        # ÉTANT DONNÉ une Porte reliée à deux Lecteurs, ayant tous les deux détecté un Badge

        lecteur1 = self.lecteur
        lecteur1.simuler_detection_badge()

        lecteur2 = self.lecteur
        lecteur2.simuler_detection_badge()

        self.moteur.associer(lecteur1, self.porte)
        self.moteur.associer(lecteur2, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS un seul signal d'ouverture est envoyé à la Porte
        self.assertTrue(self.porte.ouverture_demandee)

    def test_cas_fermeture_automatique(self):
        # ÉTANT DONNÉ une Porte ouverte, elle doit se fermer automatiquement après une période d'inactivité
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS la porte se ferme automatiquement après une période d'inactivité
        self.assertTrue(self.porte.ouverture_demandee)
        self.moteur.attendre(2)  # Utilisation de 2 secondes pour simuler l'inactivité
        self.assertFalse(self.porte.ouverture_demandee)  # La porte ne doit plus être ouverte
        self.assertTrue(self.porte.fermeture_demandee)  # La porte doit être fermée

    def test_cas_duree_ouverte(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS la porte reste ouverte pendant une durée prédéfinie
        self.assertTrue(self.porte.ouverture_demandee)
        self.moteur.attendre(3)  # Utilisation de 3 secondes pour vérifier que la porte reste ouverte
        self.assertFalse(self.porte.ouverture_demandee)  # La porte doit se fermer après la durée prédéfinie

    def test_cas_lecteur_non_associe(self):
        # ÉTANT DONNÉ un Lecteur non associé à une porte
        lecteur = LecteurTest()
        self.lecteur.simuler_detection_badge()


        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS aucune porte ne reçoit le signal d'ouverture
        self.assertEqual(len(self.moteur._portes_a_ouvrir), 0)

    def test_cas_porte_desactivee(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, self.porte)

        # Désactiver la porte
        self.moteur.desactiver(self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS le signal d'ouverture n'est pas envoyé à la porte désactivée
        self.assertFalse(self.porte.ouverture_demandee)    

    def test_cas_lecteur_avec_badge_invalide(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge invalide
        self.lecteur.simuler_detection_badge_invalide()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(self.porte.ouverture_demandee)

    def test_cas_aucune_association(self):
        # ÉTANT DONNÉ un Lecteur sans association à une Porte
        lecteur = LecteurTest()
        self.lecteur.simuler_detection_badge()


        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs
        self.moteur.interroger()

        # ALORS aucune porte ne reçoit le signal d'ouverture
        self.assertEqual(len(self.moteur._portes_a_ouvrir), 0)  

    def test_cas_horaires_ouvertures(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur, ayant détecté un Badge
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND il est interrogé dans une plage horraire
        self.moteur.interroger()

        # ALORS les portes pourront s'ouvrir en fonction de la plage d'horaire
        self.assertTrue(self.porte.ouverture_demandee)

    def test_admin_badge_hors_horaire(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur admin, ayant détecté un Badge valide en dehors des heures d'ouverture
        self.lecteur.simuler_detection_badge()
        self.lecteur.rendre_admin()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs en dehors des heures d'ouverture
        heure_hors_plage = time(20)
        self.moteur.interroger(heure_actuelle=heure_hors_plage)

        # ALORS le signal d'ouverture est envoyé à la porte
        self.assertTrue(self.porte.ouverture_demandee)

    def test_non_admin_badge_hors_horaire(self):
        # ÉTANT DONNÉ une Porte reliée à un Lecteur non admin, ayant détecté un Badge valide en dehors des heures d'ouverture
        self.lecteur.simuler_detection_badge()

        self.moteur.associer(self.lecteur, self.porte)

        # QUAND le Moteur d'Ouverture effectue une interrogation des lecteurs en dehors des heures d'ouverture
        heure_hors_plage = time(20)
        self.moteur.interroger(heure_actuelle=heure_hors_plage)

        # ALORS le signal d'ouverture n'est pas envoyé à la porte
        self.assertFalse(self.porte.ouverture_demandee)    

if __name__ == '__main__':
    unittest.main()
