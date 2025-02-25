# === Importations ===
from Recherche import Recherche
from utilities import obtenir_documents_pdf
from Bibliotheque import Bibliotheque
from pathlib import Path
from  utilities import question, trouve_similaire, question_binaire, deplacer_fichier

# === Initialisation ===

# Récupère le dossier contenant le script en cours d'exécution
dossier_projet = Path(__file__).resolve().parent
dossier_documents = dossier_projet / "Documents_Administratifs"
dossier_a_ranger = dossier_projet / "Documents_en_Attente"

liste_doc_a_ranger = obtenir_documents_pdf(dossier_a_ranger)
bib = Bibliotheque("BDD_Docs_Admin.ods", dossier_projet)

# === MAIN ===

# Rangement des documents
if len(liste_doc_a_ranger) != 0 :
    if question_binaire(str(len(liste_doc_a_ranger)) + " document(s) en attente d'être rangé(s) ont été détecté(s). Voulez-vous les ranger tout de suite ?") :
        for nom in liste_doc_a_ranger:
            bib.ajout_document(nom)




recuperation = question_binaire("Voulez-vous récupérer des documents administratifs ?")

while recuperation :
    recherche = Recherche(bib)
    recherche.trouve_doc()
    recuperation = question_binaire("Voulez-vous en récupérer un autre document ?")