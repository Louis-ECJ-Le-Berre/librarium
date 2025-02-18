class Reponse :

    def __init___(self, type, contenu):
        self.type = type
        self.contenu = contenu

    def __str__(self):
        return "Objet Réponse de type " + self.type + " contenant la string : " + self.contenu