from exceptions import LivreIndisponibleError, QuotaEmpruntDepasseError, MembreInexistantError, LivreInexistantError

class Livre:
    def __init__(self, ISBN, titre, auteur, annee, genre, statut):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = statut

class Membre:
    def __init__(self, ID, nom, livres_empruntes):
        self.ID = ID
        self.nom = nom
        if livres_empruntes is None:
            self.livres_empruntes = []
        else:
            self.livres_empruntes = livres_empruntes

class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.membres = []

    def ajouter(self, livre):
        existe_deja = False
        for l in self.livres:
            if l.ISBN == livre.ISBN:
                existe_deja = True
                print("Le livre existe deja")
                break
        if not existe_deja:
            self.livres.append(livre)
            print("le livre est ajoute")

    def supprimer(self, isbn):
        for livre in self.livres:
            if livre.ISBN == isbn:
                self.livres.remove(livre)
                print("le livre est supprime")
                break
        else:
            raise LivreInexistantError(f"Aucun livre avec ISBN {isbn} trouve.")

    def enregistrer_membre(self, membre):
        for m in self.membres:
            if m.ID == membre.ID:
                print("le membre est deja enregistre")
                break
        self.membres.append(membre)
        print("le membre est ajoute avec succe")

    def emprunter_livre(self, membre_id, isbn):
        membre = None
        for m in self.membres:
            if m.ID == membre_id:
                membre = m
                break
        if membre is None:
            raise MembreInexistantError(f"Membre ID {membre_id} introuvable.")

        livre = None
        for l in self.livres:
            if l.ISBN == isbn:
                livre = l
                break
        if livre is None:
            raise LivreInexistantError(f"Livre ISBN {isbn} introuvable.")

        if livre.statut != "disponible":
            raise LivreIndisponibleError(f"Le livre '{livre.titre}' est déjà emprunté.")

        if len(membre.livres_empruntes) >= 3:
            raise QuotaEmpruntDepasseError(f"{membre.nom} a déjà emprunté 3 livres.")

        livre.statut = "emprunte"
        membre.livres_empruntes.append(isbn)
        print(f"Livre '{livre.titre}' est emprunte")

    def retourner_livre(self, membre_id, isbn):
        membre = None
        for m in self.membres:
            if m.ID == membre_id:
                membre = m
                break
        if membre is None:
            raise MembreInexistantError(f"Membre ID {membre_id} introuvable.")

        livre = None
        for l in self.livres:
            if l.ISBN == isbn:
                livre = l
                break
        if livre is None:
            raise LivreInexistantError(f"Livre ISBN {isbn} introuvable.")

        if isbn not in membre.livres_empruntes:
            raise LivreIndisponibleError("Ce livre n est pas emprunte a ce membre.")

        livre.statut = "disponible"
        membre.livres_empruntes.remove(isbn)
        print(f"Le livre '{livre.titre}' retourné par {membre.nom}.")

    def sauvegarder_livres(self, chemin_fichier):
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            for livre in self.livres:
                ligne = f"{livre.ISBN};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.statut}\n"
                f.write(ligne)

    def charger_livres(self, chemin_fichier):
        self.livres = []
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                parts = ligne.strip().split(";")
                if len(parts) == 6:
                    isbn, titre, auteur, annee, genre, statut = parts
                    livre = Livre(isbn, titre, auteur, int(annee), genre, statut)
                    self.livres.append(livre)
    def sauvegarder_membres(self, chemin_fichier):
       with open(chemin_fichier, "w", encoding="utf-8") as f:
         for membre in self.membres:
            livres_str = ",".join(membre.livres_empruntes)  
            ligne = f"{membre.ID};{membre.nom};{livres_str}\n"
            f.write(ligne)
    def charger_membres(self, chemin_fichier):
      self.membres = []
      with open(chemin_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split(";")
            if len(parts) >= 2:
                ID, nom = parts[0], parts[1]
                livres_empruntes = parts[2].split(",") if len(parts) > 2 and parts[2] else []
                membre = Membre(ID, nom, livres_empruntes)
                self.membres.append(membre)

