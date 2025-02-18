# === Importations ===

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

from utilities import creer_ligne

class Bibliotheque :

    def __init__(self, nom_doc) :
        # Doit chercher dans le tableur excel toutes les informations pour les regrouper dans ses attributs
        self.doc = load("BDD_Docs_Admin.ods")
        self.table = self.doc.spreadsheet.getElementsByType(Table)[0]
        pass

    def ajout(self, document) :
        # Prend un objet document et l'ajoute dans la bibliothèque avec toutes ses informations

        liste_attributs = document.infos #On récupère les informations de l'objet document
        ligne = creer_ligne(liste_attributs)
        self.table.addElement(ligne)
        self.doc.save("BDD_Docs_Admin.ods")
        self.mise_a_jour()

    def mise_a_jour(self) :
        # Met à jour les informations de l'objet pour correspondre à la base de données

        self.doc = load("BDD_Docs_Admin.ods")
        self.table = self.doc.spreadsheet.getElementsByType(Table)[0]

    def write(self, square, string) :
        # Ecris le contenu de string dans la square
        pass

    def read(self, square) :
        # Renvoie ce qui est contenu dans la square
        pass

    def liste_mc(self, mc):
        # Print la liste de tous les objets qui ont le mot-clef mc
        pass