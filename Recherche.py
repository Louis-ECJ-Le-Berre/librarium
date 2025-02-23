from utilities import from_list_to_coma_string, demande_choix_mutiples, from_coma_string_to_list, affiche_liste_numero, deplacer_fichier, question_binaire
from Reponse import ReponseAnnee, ReponseMois, ReponseNature, ReponseCategorie, ReponseMC
from pathlib import Path

class Recherche:

    def __init__(self, bibli) :
        self.bibli = bibli
        self.all_docs = self.bibli.all_docs
        self.criteres = ["", "", "", "", []]
        self.doc_recherche = self.filtre()

    def __str__(self):
        str_1 = from_list_to_coma_string(self.criteres[:4])
        str_2 = from_list_to_coma_string(self.criteres[4])
        return ("Objet Recherche définie par les critères de sélection suivants : " + str_1 + " avec les mots-clefs : " + str_2)

    def filtre(self):
        """Filtre les documents à partir de la liste de critères de la classe"""
        doc_filtres = []

        for doc in self.all_docs:

            # Pour les critères nature, catégories, année et mois, il faut que ça match
            saute_doc = False
            for i in range(4):
                if self.criteres[i] != "" and self.criteres[i] != doc.infos[i] :
                    saute_doc = True
                    break
                #print(self.criteres[i], doc.infos[i], saute_doc)

            if saute_doc : continue

            # Pour les mots-clefs
            if self.criteres[4] != [] :
                passe = all(mot_clef in doc.mc for mot_clef in self.criteres[4]) # On vérifie si tous les mots-clefs sont bien présents
                if passe : doc_filtres.append(doc) #S'ils sont tous présents, on ajoute

            else : doc_filtres.append(doc) #S'il n'y a pas de filtre à mots-clefs, on ajoute le document

        self.doc_recherche = doc_filtres

        return doc_filtres
    
    def affiche_criteres(self):
        print('== Critères de recherche actuels ==')
        print('Categorie recherchee : ', self.criteres[0])
        print('Nature recherche : ', self.criteres[1])
        print('Annee recherchee : ', self.criteres[2])
        print('Mois recherche : ', self.criteres[3])
        print('Mot-clef recherche : ', from_list_to_coma_string(self.criteres[4]))
        print("")

    def change_criteres(self):
        index_choix, choix = demande_choix_mutiples('Quel critère voulez-vous ajouter/modifier ? ', ['Nature','Categorie','Année','Mois','Mot-clef'])

        if index_choix == 0 : return False
        if index_choix == 1 : r = ReponseNature(self.bibli)
        if index_choix == 2 : r = ReponseCategorie(self.bibli)
        if index_choix == 3 : r = ReponseAnnee(self.bibli)
        if index_choix == 4 : r = ReponseMois(self.bibli)
        if index_choix == 5 : r = from_coma_string_to_list(ReponseMC(self.bibli))

        self.criteres[index_choix - 1] = r.contenu

        return True

    def affiche_docs(self) :
        """Affiche les documents qui ont été filtrés en prévenant s'il y en a trop"""

        if len(self.doc_recherche) > 15 :
            print("Vos critères correspondent à " + str(len(self.doc_recherche)) + " documents. Seuls les 15 premiers sont affichés, affinez la recherche.")

        if len(self.doc_recherche) == 0 :
            print("Aucun document correspondant à vos critères")
        affiche_liste_numero(self.doc_recherche[:15])
        
    def recupere_doc(self, doc):
        """Prend le document sélectionné et l'envoi dans le dossir des fichiers à récupérer"""
        
        deplacer_fichier(doc.path, Path("Documents_Recuperes/" + doc.nom), copier = True)

    def trouve_doc(self):
        """Cherche un document à l'aide des informations de l'utilisateur et le range dans le dossier à récupérer"""
        continuer = True

        while continuer:
            if not self.change_criteres() : break
            print("")
            self.affiche_criteres()
            self.filtre()
            self.affiche_docs()

            if question_binaire("Voulez-vous affiner la recherche ?") :
                continue
            else :
                index, doc = demande_choix_mutiples("Quel document voulez-vous récupérer ?", self.doc_recherche)

                while index != 0 :
                    self.recupere_doc(doc)
                    index, doc = demande_choix_mutiples(doc.nom + " bien récupéré ! Un autre ?", self.doc_recherche)

                if not question_binaire("Voulez-vous continuer la recherche ?") : continuer = False