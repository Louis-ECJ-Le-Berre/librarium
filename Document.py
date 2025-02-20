from Reponse import Reponse

class Document :

    def __init__(self, nature, categorie, annee, mois, mots_clefs):
        """Regroupe toutes les informations contenues dans un document à partir de 5 string"""
        self.nature = nature
        self.categorie = categorie
        self.annee = annee
        self.mois = mois
        self.mc = self.nettoyer_mc(mots_clefs)
        self.infos = [nature, categorie, annee, mois, mots_clefs]

    def __str__(self):
        string = "Ce Document est un(e) " + self.nature + " dans la catégorie " + self.categorie + " datant de " + str(self.mois) + "/" + str(self.annee) + " et a pour mots-clefs : "
        for mot in self.mc :
            string += mot
            string += " ; "

        return string[:-2]

    def modify(self):
        #Modifie un des attributs du document
        pass

    def creer_nom(self):
        # Créer le nom standard du document
        pass

    def creer_path(self):
        # Créer le path où on peut trouver ce document dans la bibli
        pass

    def nettoyer_mc(self, string):
        """Prend une string de mots-clefs lue depuis la table avec espace et ; et la transforme en une vraie liste de mots-clefs"""

        new_string = string.replace(" ","")
        liste = new_string.split(";")
        return liste