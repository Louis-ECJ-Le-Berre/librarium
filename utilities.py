from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import readline

def demande(question, liste_auto_completion = []):
    """Fais une demande à un utilisateur en permettant l'auto-complétion par l'ajout en argument d'une liste de mots, et retourne la réponse"""
    def completer_texte(texte_saisi, etat):
        options = [mot for mot in liste_auto_completion if mot.lower().startswith(texte_saisi.lower())]
        if etat < len(options):
            return options[etat]
        return None

    # Activer l'auto-complétion
    readline.parse_and_bind("tab: menu-complete")  # Permet la navigation entre options
    readline.parse_and_bind("set show-all-if-ambiguous on")  # Affiche les options dès le 1er Tab
    readline.parse_and_bind("set completion-ignore-case on")  # Ignore la casse
    readline.set_completer(completer_texte)

    # Demander une information avec auto-complétion
    return input(question)

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