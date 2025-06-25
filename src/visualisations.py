import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from datetime import datetime, timedelta

def graphe_genres(livres):
    genres = [livre.genre for livre in livres]
    compteur = Counter(genres)
    
    plt.figure(figsize=(6,6))
    plt.pie(compteur.values(), labels=compteur.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Pourcentage des livres par genre")
    plt.savefig("assets/stats_genres.png")
    plt.close()

def graphe_auteurs(livres):
    auteurs = [livre.auteur for livre in livres]
    top = Counter(auteurs).most_common(10)

    noms = [a[0] for a in top]
    quantites = [a[1] for a in top]

    plt.figure(figsize=(10,5))
    plt.bar(noms, quantites, color="green")
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 des auteurs les plus populaires")
    plt.ylabel("Nombre de livres")
    plt.tight_layout()
    plt.savefig("assets/stats_auteurs.png")
    plt.close()

def courbe_emprunts(fichier_historique):
    df = pd.read_csv(fichier_historique)
    df["date"] = pd.to_datetime(df["date"])
    
    date_limite = datetime.today() - timedelta(days=30)
    df_recent = df[(df["date"] >= date_limite) & (df["action"] == "emprunt")]

    stats = df_recent.groupby(df_recent["date"].dt.date).size()

    plt.figure(figsize=(10,4))
    stats.plot(kind="line", marker="o")
    plt.title("Emprunts (30 derniers jours)")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("assets/stats_temps.png")  
    plt.close()

def generer_statistiques(biblio, chemin_historique="data/historique.csv"):
    graphe_genres(biblio.livres)
    graphe_auteurs(biblio.livres)
    courbe_emprunts(chemin_historique)
