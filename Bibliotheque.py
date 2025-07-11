# === Importations ===

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from numpy import sort
from Reponse import ReponseAnnee, ReponseMois, ReponseNature, ReponseCategorie, ReponseMC
from Recherche import Recherche
import os

from utilities import creer_ligne, lire_ligne, question_binaire, affiche_document, deplacer_fichier

from Document import Document

class Bibliotheque :

    def __init__(self, nom_BDD, project_path) :
        # Doit chercher dans le tableur excel toutes les informations pour les regrouper dans ses attributs
        self.bdd = load(nom_BDD)
        self.table = self.bdd.spreadsheet.getElementsByType(Table)[0]
        self.all_docs = self.get_all_documents(self.table)
        self.all_mc = self.get_all_mc()
        self.all_nature = self.get_all_nature()
        self.project_path = project_path

    def ajout_document(self, nom_du_doc):
        """Demande les informations et crée le document dans la bibliothèque"""

        # Récupère le path du document à ranger et l'affiche
        old_path = self.project_path / "Documents_en_Attente" / nom_du_doc
        affiche_document(old_path)

        if question_binaire("Voulez-vous l'ajouter ?"):
            # Crée le document, l'ajoute et le sauvegarde
            mois = ReponseMois(self).contenu
            annee = ReponseAnnee(self).contenu
            categorie = ReponseCategorie(self).contenu
            nature = ReponseNature(self).contenu
            mc = ReponseMC(self, nature, self.get_mc_selon_nature(nature)).contenu
            document = Document(nature, categorie, annee, mois, mc)
            

            # Essaye de déplacer le document à sa nouvelle place
            
            if self.deplacer_document(document, old_path):
                self.sauvegarde_document(document) #Si le fichier a pu être déplacé (et donc pas de doublon) on enregistre dans la base

    def deplacer_document(self, doc, old_path):
        """Essaye de déplacer le document et propose de le remplacer si déjà existant"""
        new_path = self.project_path / "Documents_Administratifs" / doc.path
        return deplacer_fichier(old_path, new_path)


    def sauvegarde_document(self, document) :
        """Prend un objet document et l'ajoute dans la bibliothèque avec toutes ses informations. 
        Renvoie un objet bibliohtèque mis à jour selon la nouvelle base de données"""

        liste_attributs = document.infos #On récupère les informations de l'objet document
        ligne = creer_ligne(liste_attributs)
        self.table.addElement(ligne)
        self.bdd.save("BDD_Docs_Admin.ods")

        
        # Pour mettre à jour les tables en attendant la prochaine fois où on recrée un objet bibliothèque qui utilisera le nouveau tableur tout neuf
        self.all_docs.append(document)
        self.all_mc = self.get_all_mc()
        self.all_nature = self.get_all_nature()

    def lit_document(self, odfpy_row):
        """Prend une ligne de type odfpy, en lit les cellules et renvoie un objet document"""

        liste = lire_ligne(odfpy_row)

        try :
            doc = Document(liste[0],liste[1],liste[2],liste[3],liste[4])
            return doc
        except :
            print("Une erreur est survenue pour créer un document à partir de la liste : ")
            print(liste)  
            print("Création d'un document vide")
            return Document()
    
    def write(self, square, string) :
        # Ecris le contenu de string dans la square
        pass

    def read(self, square) :
        # Renvoie ce qui est contenu dans la square
        pass

    def liste_par_mc(self,mc):
        """Renvoie une liste de tous les documents contenant un mot-clef particulier"""

        liste_doc = []

        for doc in self.all_docs :
            if mc in doc.mc :
                liste_doc.append(doc)

        return liste_doc
        

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
    
    def get_mc_selon_nature(self, nature):
        doc_filtre = Recherche(self, nature).doc_recherche

        liste_mc = []

        for doc in doc_filtre:
            liste_mc.extend(doc.mc)

        liste_unique = list(set(liste_mc))
        sort(liste_unique)

        return liste_unique
