from  utilities import question

class Reponse :

    def __init__(self, type):
        self.type = type
        self.categories_existantes = ["Assurances", "Citoyenneté", "Finances", "Logement", "Mobilité", "Education", "Santé", "Travail", "Famille", "Retraite", "Justice", "Culture"]
        self.contenu = self.demande()

        while not self.est_valide():
            self.contenu = self.redemande()

        self.formatage()

    def __str__(self):
        return "Objet Réponse de type " + self.type + " contenant la string : " + self.contenu
    
    def formatage(self):
        """Traite la réponse de l'utilisateur et la formate pour qu'elle puisse être utilisée correctement pour créer un objet"""

        #Le principe est qu'on peut se baser sur des fonctions définies uniquement dan sles sous-classes


class ReponseMois(Reponse) :

    def __init__(self):
        super().__init__("Mois")
        
    def est_valide(self):
        """Renvoie True ou False selon que la valeur est bien correcte pour un mois"""
        try :
            reponse_chiffre = int(self.contenu)
        except ValueError :
            return False

        if reponse_chiffre <= 12 and reponse_chiffre > 0 :
            if len(self.contenu) == 2 :
                return True

        return False
    
    def demande(self):

        return question('Mois du document (01, 08, 11, ...) ?')

    def redemande(self):
        print('\nVeuillez ressaisir une Année (Rappel : un nombre à 2 chiffres entre 01 et 12 est attendu)')
        return self.demande()
    
    def formatage(self):
        """Enlève tous les espaces"""

        self.contenu.replace(" ","")
        return True

        
    
class ReponseAnnee(Reponse):

    def __init__(self):
        super().__init__("Année")

    def est_valide(self):
        """Renvoie True ou False selon que la valeur est bien correcte pour une année"""

        try :
            int(self.contenu)
        except ValueError :
            return False

        if len(self.contenu) == 4 :
            return True
        return False
    
    def demande(self):

        return question('Année du document ?')

    def redemande(self):
        print('\nVeuillez ressaisir une Année (Rappel : un nombre à 4 chiffres est attendu)')
        return self.demande()
    
    def formatage(self):
        """Enlève tous les espaces"""

        self.contenu.replace(" ","")

        return True
    
class ReponseNature(Reponse):

    def __init__(self):
        super().__init__("Nature")

    def est_valide(self):
        """Renvoie True ou False selon que la valeur est bien correcte pour une nature"""

        if ' ' in self.contenu : return False

        return True

    def demande(self):
        return question('Nature du document ?')

    def redemande(self):
        print('\nVeuillez ressaisir une Nature (un ensemble de mots séparés uniquement par des symboles _ est attendu)')
        return self.demande()
    
    def formatage(self):
        """Scinde une expression selon les _ , met tout en minuscules et une majuscule devant chaque mot"""

        mot_formate = ''
        saisie_scindee = self.contenu.split('_')

        for mot in saisie_scindee :

            mot = mot.lower()
            mot = mot[0].upper() + mot[1:]
            mot_formate += mot + '_'

        self.contenu = mot_formate[:-1]
        return True
    
class ReponseCategorie(Reponse):

    def __init__(self):
        super().__init__("Catégorie")

    def est_valide(self):
        
        if self.contenu in self.categories_existantes :
            return True
        return False
    
    def demande(self):
        return question('Catégorie à laquelle appartient le document ?', self.categories_existantes)
    
    def redemande(self):
        string_cat = ""
        for cat in self.categories_existantes : string_cat += cat + "\n"
        print('\nVeuillez ressaisir une Catégorie. Pour rappel, les catégories sont : \n' + string_cat[:-1])
        return self.demande()
    
    def formatage(self):
        """Met une majuscule au début et le reste en minuscule"""

        self.contenu = self.contenu.lower()
        self.contenu = self.contenu[0].upper() + self.contenu[1:]

        return True