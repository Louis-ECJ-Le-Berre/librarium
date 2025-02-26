from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import readline
from difflib import get_close_matches
import os
from pathlib import Path
import subprocess
import sys
import shutil
import numpy as np

def trouve_similaire(mot_propose, liste_mots = []):
    """Trouve le mots le plus similaires à un mot donné parmi une liste de mots"""
    similarites_trouvees = get_close_matches(mot_propose, liste_mots, 1, cutoff=0.6)
    if len(similarites_trouvees) != 0 and similarites_trouvees[0] != mot_propose :
        return similarites_trouvees[0]
    else :
        return []


def auto_completion(liste_auto_completion = []):
    """Met en place l'auto-complétion"""

    def completer_texte(texte_saisi, etat):
        options = [mot for mot in liste_auto_completion if mot.lower().startswith(texte_saisi.lower())]
        if etat == 0 and len(options) > 1:
            print("\n \nSuggestions :")
            for opt in options:
                print(f"  {opt}")
            print()  # Ligne vide pour séparation
    
        return options[etat] if etat < len(options) else None

    # Activer l'auto-complétion
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer_texte)

def question(question, liste_a_comparer = []):
    """Fais une demande à un utilisateur en permettant l'auto-complétion et en notant si un mot est similaire"""
    
    auto_completion(liste_a_comparer) #Active l'auto-complétion
    # Demander une information avec auto-complétion
    print('')
    print(question + ' : ')
    return str(input())

def question_binaire(question):
    """Pose une question binaire à l'utilisateur et renvoie sa réponse sous forme de booléen"""

    print('')
    print(question + '  [o/n]   ')

    reponse = input()

    if reponse == 'O' or reponse == 'o' or reponse =='oui':
        return True

    elif reponse == 'N' or reponse == 'n' or reponse == 'non':
        return False

    else :

        print('\n Répondez par O (pour oui) ou N (pour Non) \n')
        return question_binaire(question)
    

def creer_ligne(liste_elements):
    """Renvoie une odfpy row contenant dans chaque cellule un élément de la liste fournie en entrée"""
    ligne = TableRow()

    for element in liste_elements:
        nouvelle_cellule = TableCell()

        if not isinstance(element,list):
            nouvelle_cellule.addElement(P(text=element))

        else :
            string = ""
            for mc in element :
                string += mc
                string += " ; "
            nouvelle_cellule.addElement(P(text=string))

        ligne.addElement(nouvelle_cellule)
    
    return ligne

def lire_ligne(odfpy_row):
    """Prend une odfpy row et renvoie une liste contenant pour chaque élément le contenu d'une cellule"""

    liste = []

    for cellule in odfpy_row.getElementsByType(TableCell):
        text_elements = cellule.getElementsByType(P)
        if text_elements:
            liste.append(text_elements[0].firstChild.data)  # Ajouter le texte
        else:
            liste.append("")

    return liste

def from_list_to_coma_string(liste):
    """Transforme une liste en une string contenant chaque élément séparé par un ;"""
    string = ""

    for m in liste:
        string += m + " ; "

    return string[:-2]

def from_coma_string_to_list(string):
    """Prend une string de mots-clefs lue depuis la table avec espace et ; et la transforme en une vraie liste de mots-clefs"""

    new_string = string.replace(" ","")
    liste = new_string.split(";")
    return liste
    
def affiche_document(path_doc):
    """Ouvre un document en fonction du système d'exploitation en donnant un Path WSL ou une string"""

    path_doc = Path(path_doc)  # Assure que c'est un Path
    subprocess.Popen(["evince", path_doc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def obtenir_documents_pdf(dossier):
    """Retourne une liste des noms de fichiers PDF dans le dossier spécifié"""
    if not os.path.exists(dossier):
        print(f"Erreur : Le dossier {dossier} n'existe pas.")
        return []
    
    # Liste les noms des fichiers PDF
    return [f for f in os.listdir(dossier) if f.endswith('.pdf')]

def element_en_commun(liste_1, liste_2):
    """Regarde si deux listes ont au moins un élément en commun"""
    common = set(liste_1) & set(liste_2)

    if common:
        return True
    else:
        return False
    
def demande_choix_mutiples(question, liste_reponses, tri = True) :
    """Pose une question à choix multiples à l'utilisateur et renvoie l'index et la réponse associée"""
    liste = ['Retour en arrière']
    

    if tri :
        liste.extend(np.sort(liste_reponses))
    else :
        liste.extend(liste_reponses)
    
    i=0
    print('')
    print(question)

    affiche_liste_numero(liste, False)

    print('\n Sélectionnez le numéro correspondant à votre choix')

    reponse = input()

    try :
        x = int(reponse)
    except ValueError :
        print('\n Répondez uniquement par un nombre\n')
        return demande_choix_mutiples(question, liste, tri)

    if x < len(liste) :
        return x, liste[x]
    elif x == liste :
        return False

    else :
        print('\n Votre réponse ne fait pas partie des nombres proposés\n')
        return demande_choix_mutiples(question, liste_reponses, tri)
    
def affiche_liste_numero(liste, tri = True) :
    """Affiche les éléments d'une liste en les numérotant et en les mettant par ordre alphabétique"""
    i=0
    if tri :
        liste = np.sort(liste)

    for i,choix in enumerate(liste):
        if isinstance(choix, str) :
            print('[ ' + str(i) + ' ]   ' + choix)
        else :
            print('[ ' + str(i) + ' ]   ' + choix.nom)

def deplacer_fichier(old_path, new_path, copier=False):
    """Essaye de déplacer ou de copier un fichier d'un point à un autre et propose de le remplacer si déjà existant.

    Arguments :
    old_path : Path — Chemin du fichier source.
    new_path : Path — Chemin de destination du fichier.
    copier : bool — Si True, copie le fichier au lieu de le déplacer. Par défaut, c'est un déplacement.
    """

    if not old_path.exists():
        print(f"❌ Le fichier source n'existe pas : {old_path}")
        return False

    # Vérifie que le dossier cible existe, sinon le crée
    if not new_path.parent.exists():
        new_path.parent.mkdir(parents=True, exist_ok=True)
    
    if new_path.exists():
        # Si le fichier existe déjà, on propose de le remplacer
        affiche_document(new_path)
        if question_binaire(f"Le chemin {new_path} est déjà occupé par un fichier. Souhaitez-vous le remplacer ?"):
            try:
                if copier:
                    shutil.copy2(old_path, new_path)  # Copie le fichier avec ses métadonnées
                    print(f"✅ Le fichier a été copié à : {new_path}")
                else:
                    old_path.replace(new_path)  # Remplace le fichier existant
                    print(f"✅ Le fichier a été remplacé à : {new_path}")
                return True
            except Exception as e:
                print(f"❌ Une erreur est survenue lors de l'opération : {e}")
                return False
        else:
            print("❌ Le fichier n'a pas été copié ou déplacé.")
            return False
        
    else:
        try:
            if copier:
                shutil.copy2(old_path, new_path)  # Copie le fichier avec ses métadonnées
                print(f"✅ Le fichier a été copié à : {new_path}")
            else:
                old_path.rename(new_path)  # Déplace le fichier
                print(f"✅ Le fichier a été déplacé vers : {new_path}")
            return True
        
        except Exception as e:
            print(f"❌ Une erreur est survenue lors de l'opération : {e}")
            return False

