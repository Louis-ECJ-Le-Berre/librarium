# === Importations ===

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from numpy import sort
from Reponse import Reponse, ReponseMois

from utilities import creer_ligne, lire_ligne

from Document import Document

class Bibliotheque :

    def __init__(self, nom_BDD) :
        # Doit chercher dans le tableur excel toutes les informations pour les regrouper dans ses attributs
        self.bdd = load(nom_BDD)
        self.table = self.bdd.spreadsheet.getElementsByType(Table)[0]
        self.all_docs = self.get_all_documents(self.table)
        self.all_mc = self.get_all_mc()

    def ajout_document(self):
        """Demande les informations et crée le document dans la bibliothèque"""

        mois = ReponseMois(15)

    def sauvegarde_document(self, document) :
        """Prend un objet document et l'ajoute dans la bibliothèque avec toutes ses informations. 
        Renvoie un objet bibliohtèque mis à jour selon la nouvelle base de données"""

        liste_attributs = document.infos #On récupère les informations de l'objet document
        ligne = creer_ligne(liste_attributs)
        self.table.addElement(ligne)
        self.bdd.save("BDD_Docs_Admin.ods")
        
        return Bibliotheque("BDD_Docs_Admin.ods")

    def lit_document(self, odfpy_row):
        """Prend une ligne de type odfpy, en lit les cellules et renvoie un objet document"""

        liste = lire_ligne(odfpy_row)
        return Document(liste[0],liste[1],liste[2],liste[3],liste[4])
    
    def write(self, square, string) :
        # Ecris le contenu de string dans la square
        pass

    def read(self, square) :
        # Renvoie ce qui est contenu dans la square
        pass

    def liste_par_mc(self,mc):
        """Renvoie une liste de tous les documents contenant un mot-clef particulier"""
        

    def get_all_mc(self):
        """Récupère la liste de tous les mots-clefs présents dans la table, et les trie par ordre alphabétique"""

        liste_mc = []

        for doc in self.all_docs:
            liste_mc.extend(doc.mc)

        liste_unique = list(set(liste_mc))
        return sort(liste_unique)
    
    def get_all_nature(self):
        """Récupère la liste de toutes les natures de documents dans la table, et les trie par ordre alphabétique"""

        liste_nature = []

        for doc in self.all_docs:
            liste_nature.append(doc.nature)

        liste_unique = list(set(liste_nature))
        return sort(liste_unique)


    def get_all_documents(self, table):
        """Prend une table de type odfpy et renvoie une liste contenant tous les documents de cette table"""

        liste_documents = []
        rows = table.getElementsByType(TableRow)

        for ligne in rows :
            new_doc = self.lit_document(ligne)
            liste_documents.append(new_doc)

        return liste_documents