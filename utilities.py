from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

def creer_ligne(liste_elements):
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
