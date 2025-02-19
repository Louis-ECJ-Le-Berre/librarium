from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

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