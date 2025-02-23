from  utilities import question, trouve_similaire, question_binaire, from_list_to_coma_string

class Reponse :

    def __init__(self, type, bibli):
        self.type = type
        self.categories_existantes = ["Assurances", "Citoyenneté", "Finances", "Logement", "Mobilité", "Education", "Santé", "Travail", "Famille", "Retraite", "Justice", "Culture"]
        self.mc_existants = bibli.all_mc
        self.natures_existantes = bibli.all_nature
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

    def __init__(self, bibli):
        super().__init__("Mois", bibli)
        
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

    def __init__(self, bibli):
        super().__init__("Année", bibli)

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

    def __init__(self, bibli):
        super().__init__("Nature", bibli)

    def est_valide(self):
        """Renvoie True ou False selon que la valeur est bien correcte pour une nature"""

        if ' ' in self.contenu : return False

        return True

    def demande(self):
        return question('Nature du document ?', self.natures_existantes)

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

    def __init__(self, bibli):
        super().__init__("Catégorie", bibli)

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
    
class ReponseMC(Reponse):

    def __init__(self, bibli):
        super().__init__("Mots-Clés", bibli)
    
    def est_valide(self):

        if "  " in self.contenu:
            return False
        
        return True

    def demande(self):
        return question('Quels sont les mots-clefs attachés à ce document ?', self.mc_existants)
    
    def redemande(self):
        print('\nVeuillez ressaisir un ou plusieurs mots-clefs (chaque mot-clef peut être constitué de plusieurs mots séparés par des _ et chaque mot-clef est séparé par un espace)')
        return self.demande()
    
    def formatage(self):
        """Met une majuscule devant chaque mot de chaquem mot-clef et les sépare par des ; pour pouvoir être utilisés pour faire un document"""

        mc_scindes = self.contenu.split(" ")
        mc_final = ""

        for mc in mc_scindes :
            mot_formate = ""
            mot_scinde = mc.split("_")

            for mot in mot_scinde :
                mot = mot.lower()
                mot = mot[0].upper() + mot[1:]
                mot_formate += mot + '_'

            mc_final += mot_formate[:-1] + " ; "

        self.contenu = self.change_si_similaire(mc_final[:-3])

    def change_si_similaire(self, saisie_mc):
        """Regarde si parmi la saisie de mots-clefs il s'en trouve des similaires à des mots-clefs existans déjà et si l'utilisateur ne veut pas modifier sa saisie"""
        
        liste_mc = saisie_mc.split(" ; ")

        for i in range(len(liste_mc)) :
            mot = liste_mc[i]
            if mot != "" :
                similaire = trouve_similaire(mot, self.mc_existants)
                if len(similaire) != 0 :
                    if question_binaire("Le mot-clef -- " + similaire + " -- se trouve déjà dans la base de données. Voulez-vous remplacer -- " + mot + " -- par ce mot-clef déjà existant ?"):
                        liste_mc[i] = similaire

        return from_list_to_coma_string(liste_mc)

