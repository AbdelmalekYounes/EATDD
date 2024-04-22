class AssociationsLecteurPorte:
    def __init__(self):
        self.associations = {}

    def enregistrer(self, lecteur, porte):
        if lecteur in self.associations:
            self.associations[lecteur].add(porte)
        else:
            self.associations[lecteur] = {porte}

