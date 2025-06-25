import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from bibliotheque import Bibliotheque, Livre, Membre
from visualisations import graphe_genres, graphe_auteurs  

class BibliothequeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Bibliothèque")

        self.biblio = Bibliotheque()

        try:
            self.biblio.charger_livres("data/Livres.txt")
        except FileNotFoundError:
            pass

        try:
            self.biblio.charger_membres("data/membre.txt")  
        except FileNotFoundError:
            pass
        
        graphe_genres(self.biblio.livres)
        graphe_auteurs(self.biblio.livres)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.frame_livres = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_livres, text="Livres")
        self.creer_onglet_livres()

        self.frame_membres = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_membres, text="Membres")
        self.creer_onglet_membres()

        self.frame_stats = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_stats, text="Statistiques")
        self.creer_onglet_stats()

        self.actualiser_liste_livres()
        self.actualiser_liste_membres()

    def creer_onglet_livres(self):
        colonnes = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Statut")
        self.tree_livres = ttk.Treeview(self.frame_livres, columns=colonnes, show="headings")
        for col in colonnes:
            self.tree_livres.heading(col, text=col)
            self.tree_livres.column(col, width=100)
        self.tree_livres.pack(fill='both', expand=True, pady=10)

        form_frame = ttk.Frame(self.frame_livres)
        form_frame.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="ISBN").grid(row=0, column=0, padx=5, pady=2)
        self.isbn_entry = ttk.Entry(form_frame)
        self.isbn_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Titre").grid(row=1, column=0, padx=5, pady=2)
        self.titre_entry = ttk.Entry(form_frame)
        self.titre_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Auteur").grid(row=2, column=0, padx=5, pady=2)
        self.auteur_entry = ttk.Entry(form_frame)
        self.auteur_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Année").grid(row=3, column=0, padx=5, pady=2)
        self.annee_entry = ttk.Entry(form_frame)
        self.annee_entry.grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Genre").grid(row=4, column=0, padx=5, pady=2)
        self.genre_entry = ttk.Entry(form_frame)
        self.genre_entry.grid(row=4, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Statut").grid(row=5, column=0, padx=5, pady=2)
        self.statut_entry = ttk.Combobox(form_frame, values=["disponible", "emprunte"])
        self.statut_entry.current(0)
        self.statut_entry.grid(row=5, column=1, padx=5, pady=2)

        ajouter_btn = ttk.Button(form_frame, text="Ajouter Livre", command=self.ajouter_livre)
        ajouter_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def creer_onglet_membres(self):
        colonnes = ("ID", "Nom", "Livres empruntés")
        self.tree_membres = ttk.Treeview(self.frame_membres, columns=colonnes, show="headings")
        for col in colonnes:
            self.tree_membres.heading(col, text=col)
            self.tree_membres.column(col, width=150)
        self.tree_membres.pack(fill='both', expand=True, pady=10)

        form_frame = ttk.Frame(self.frame_membres)
        form_frame.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="ID").grid(row=0, column=0, padx=5, pady=2)
        self.id_entry = ttk.Entry(form_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Nom").grid(row=1, column=0, padx=5, pady=2)
        self.nom_entry = ttk.Entry(form_frame)
        self.nom_entry.grid(row=1, column=1, padx=5, pady=2)

        ajouter_btn = ttk.Button(form_frame, text="Ajouter Membre", command=self.ajouter_membre)
        ajouter_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def creer_onglet_stats(self):
        ttk.Label(self.frame_stats, text="Statistiques de la bibliothèque", font=("Arial", 14)).pack(pady=10)

        try:
            img1 = Image.open("assets/stats_genres.png")
            img2 = Image.open("assets/stats_auteurs.png")

            self.img1_tk = ImageTk.PhotoImage(img1.resize((300, 200)))
            self.img2_tk = ImageTk.PhotoImage(img2.resize((300, 200)))

            ttk.Label(self.frame_stats, image=self.img1_tk).pack(pady=5)
            ttk.Label(self.frame_stats, image=self.img2_tk).pack(pady=5)

        except FileNotFoundError:
            ttk.Label(self.frame_stats, text="Fichiers de statistiques non trouvés.").pack(pady=10)

    def actualiser_liste_livres(self):
        for i in self.tree_livres.get_children():
            self.tree_livres.delete(i)
        for livre in self.biblio.livres:
            self.tree_livres.insert("", "end", values=(livre.ISBN, livre.titre, livre.auteur, livre.annee, livre.genre, livre.statut))

    def actualiser_liste_membres(self):
     for i in self.tree_membres.get_children():
        self.tree_membres.delete(i)

     print(f"Nombre de membres chargés : {len(self.biblio.membres)}")
     for membre in self.biblio.membres:
        print(f"Membre: ID={membre.ID}, Nom={membre.nom}, Livres empruntés={membre.livres_empruntes}")
        livres = ", ".join(membre.livres_empruntes) if membre.livres_empruntes else "Aucun"
        self.tree_membres.insert("", "end", values=(membre.ID, membre.nom, livres))

    def ajouter_livre(self):
        isbn = self.isbn_entry.get().strip()
        titre = self.titre_entry.get().strip()
        auteur = self.auteur_entry.get().strip()
        annee = self.annee_entry.get().strip()
        genre = self.genre_entry.get().strip()
        statut = self.statut_entry.get()

        if not (isbn and titre and auteur and annee):
            messagebox.showerror("Erreur", "ISBN, Titre, Auteur et Année sont obligatoires.")
            return

        try:
            annee = int(annee)
        except ValueError:
            messagebox.showerror("Erreur", "Année doit être un nombre entier.")
            return

        livre = Livre(isbn, titre, auteur, annee, genre, statut)
        self.biblio.ajouter(livre)
        self.actualiser_liste_livres()
        messagebox.showinfo("Succès", f"Livre '{titre}' ajouté avec succès.")

    def ajouter_membre(self):
        id_membre = self.id_entry.get().strip()
        nom = self.nom_entry.get().strip()

        if not id_membre or not nom:
            messagebox.showerror("Erreur", "ID et Nom sont obligatoires.")
            return

        membre = Membre(id_membre, nom, [])
        self.biblio.enregistrer_membre(membre)
        self.actualiser_liste_membres()
        messagebox.showinfo("Succès", f"Membre '{nom}' ajouté avec succès.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliothequeGUI(root)
    root.mainloop()
