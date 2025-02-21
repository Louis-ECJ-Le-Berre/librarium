from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import readline
from difflib import get_close_matches

def trouve_similaire(mot_propose, liste_mots = []):
    """Trouve le mots le plus similaires à un mot donné parmi une liste de mots"""
    similarites_trouvees = get_close_matches(mot_propose, liste_mots, 1)
    if len(similarites_trouvees) != 0 :
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
    print(question + '  [O/N]   ')

    reponse = input()

    if reponse == 'O' or reponse == 'o' or reponse =='oui':
        print('\n')
        return True

    elif reponse == 'N' or reponse == 'n' or reponse == 'non':
        print('\n')
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
