# === Importations ===

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

from utilities import creer_ligne

from Document import Document

class Bibliotheque :

    def __init__(self, nom_BDD) :
        # Doit chercher dans le tableur excel toutes les informations pour les regrouper dans ses attributs
        self.bdd = load(nom_BDD)
        self.table = self.bdd.spreadsheet.getElementsByType(Table)[0]
        self.all_docs = self.get_all_documents(self.table)


    def ajout(self, document) :
        """Prend un objet document et l'ajoute dans la bibliothèque avec toutes ses informations. 
        Renvoie un objet bibliohtèque mis à jour selon la nouvelle base de données"""

        liste_attributs = document.infos #On récupère les informations de l'objet document
        ligne = creer_ligne(liste_attributs)
        self.table.addElement(ligne)
        self.bdd.save("BDD_Docs_Admin.ods")
        
        return Bibliotheque("BDD_Docs_Admin.ods")

    def write(self, square, string) :
        # Ecris le contenu de string dans la square
        pass

    def read(self, square) :
        # Renvoie ce qui est contenu dans la square
        pass

    def liste_mc(self, mc):
        # Print la liste de tous les objets qui ont le mot-clef mc
        pass

    def get_all_documents(self, table):
        """Prend une table de type odfpy et renvoie une liste contenant tous les documents de cette table"""

        liste_documents = []
        rows = table.getElementsByType(TableRow)

        for ligne in rows :
            new_doc = self.create_document_from_row(ligne)
            liste_documents.append(new_doc)

        return liste_documents


    def create_document_from_row(self, odfpy_row):
        """Prend une ligne de type odfpy, en lit les cellules et renvoie un objet document"""

        liste = []

        for cellule in odfpy_row.getElementsByType(TableCell):
            text_elements = cellule.getElementsByType(P)
            if text_elements:
                liste.append(text_elements[0].firstChild.data)  # Ajouter le texte
            else:
                liste.append("")

        return Document(liste[0],liste[1],liste[2],liste[3],liste[4])