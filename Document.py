class Document :

    def __init__(self, nature, categorie, annee, mois, mots_clefs=[]):
        # Regroupe toutes les informations contenues dans un document
        self.nature = nature
        self.categorie = categorie
        self.annee = annee
        self.mois = mois
        self.mc = mots_clefs
        self.infos = [nature, categorie, annee, mois, mots_clefs]

    def __init__(self, liste_infos):

        self.infos = liste_infos
        self.nature = liste_infos[0]
        self.categorie = liste_infos[1]
        self.annee = liste_infos[2]
        self.mois = liste_infos[3]
        self.mc = liste_infos[4]

    def modify(self):
        #Modifie un des attributs du document
        pass

    def creer_nom(self):
        # Créer le nom standard du document
        pass

    def creer_path(self):
        # Créer le path où on peut trouver ce document dans la bibli
        pass