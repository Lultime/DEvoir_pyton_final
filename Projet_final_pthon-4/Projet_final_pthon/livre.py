import json
import random
from emprunt_manager import FichierManager
import datetime
import re

class Livre:
    def __init__(self, titre, auteur, genre, annee):
        self.__id = "LIV" + str(random.randint(1000, 9999))
        self.__titre = titre
        self.__auteur = auteur
        self.__genre = genre
        self.__annee = annee

    def get_id(self):
        return self.__id

    def get_titre(self):
        return self.__titre

    def get_auteur(self):
        return self.__auteur

    def get_genre(self):
        return self.__genre

    def get_annee(self):
        return self.__annee

    def to_dict(self):
        return {"id": self.__id, "titre": self.__titre, "auteur": self.__auteur, "genre": self.__genre, "annee": self.__annee}


class LivreManager:
    def __init__(self):
        self.fichier = FichierManager("livres.json")
        self.livres = self.fichier.charger()



    def ajouter_livre(self):
        genres_valides = ["Roman", "Science-Fiction", "Policier", "Fantastique", "Histoire", "Biographie"]

        # Vérification du titre (minimum 3 caractères, lettres et espaces uniquement)
        while True:
            titre = input("Titre du livre (au moins 3 lettres, pas de chiffres ni de caractères spéciaux) : ").strip()
            if len(titre) >= 3 and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", titre):
                break
            print("❌ Le titre doit contenir au moins 3 lettres et ne pas inclure de chiffres ou caractères spéciaux.")

        # Vérification de l'auteur (minimum 3 caractères, lettres et espaces uniquement)
        while True:
            auteur = input("Auteur (au moins 3 lettres, pas de chiffres ni de caractères spéciaux) : ").strip()
            if len(auteur) >= 3 and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", auteur):
                break
            print(
                "❌ Le nom de l'auteur doit contenir au moins 3 lettres et ne pas inclure de chiffres ou caractères spéciaux.")

        # Vérification du genre (choix dans une liste prédéfinie)
        while True:
            print("Genres disponibles :")
            for genre in genres_valides:
                print(f"- {genre}")
            genre = input("Genre : ").strip()
            if genre in genres_valides:
                break
            print("❌ Genre invalide. Veuillez choisir un genre dans la liste.")

        # Vérification de l'année de publication (nombre entre 1500 et l'année actuelle)
        annee_actuelle = datetime.datetime.now().year
        while True:
            annee = input(f"Année de publication (entre 1500 et {annee_actuelle}) : ").strip()
            if annee.isdigit() and 1500 <= int(annee) <= annee_actuelle:
                break
            print(f"❌ L'année doit être un nombre entre 1500 et {annee_actuelle}.")

        # Création et enregistrement du livre
        livre = Livre(titre, auteur, genre, annee)
        self.livres.append(livre.to_dict())
        self.fichier.sauvegarder(self.livres)
        print(f"✅ Livre ajouté avec ID {livre.get_id()}")

    def afficher_livres(self):
        if not self.livres:
            print("📖 Aucun livre disponible.")
            return

        for livre in self.livres:
            print(f"ID : {livre['id']}")
            print(f"Titre : {livre['titre']}")
            print(f"Auteur : {livre['auteur']}")
            print(f"Genre : {livre['genre']}")
            print(f"Année : {livre['annee']}")
            print("-" * 30)


    def rechercher_livre(self):
            # Vérification du critère de recherche
            options_valides = ["titre", "auteur", "genre"]

            while True:
                genre = input("Rechercher par (titre/auteur/genre) : ").strip().lower()
                if genre in options_valides:
                    break
                print("❌ Option invalide. Veuillez choisir entre 'titre', 'auteur' ou 'genre'.")

            valeur = input(f"Entrez la valeur du {genre} : ").strip().lower()

            # Recherche avec vérification que la clé existe dans chaque livre
            resultats = [livre for livre in self.livres if genre in livre and valeur in livre[genre].lower()]

            # Affichage des résultats
            if resultats:
                print("\n📚 Livres trouvés :")
                for livre in resultats:
                    print(f"ID : {livre.get('id', 'N/A')}")
                    print(f"Titre : {livre.get('titre', 'Inconnu')}")
                    print(f"Auteur : {livre.get('auteur', 'Inconnu')}")
                    print(f"Genre : {livre.get('genre', 'Non spécifié')}")
                    print(f"Année : {livre.get('annee', 'Non spécifiée')}")
                    print("-" * 30)
            else:
                print("❌ Aucun livre trouvé.")

    def supprimer_livre(self):
        self.afficher_livres()
        id_livre = input("ID du livre à supprimer: ")
        self.livres = [l for l in self.livres if l["id"] != id_livre]
        self.fichier.sauvegarder(self.livres)
        print("✅ Livre supprimé!")



    def modifier_livre(self):
        self.afficher_livres()
        id_livre = input("ID du livre à modifier: ").strip()

        for livre in self.livres:
            if livre["id"] == id_livre:
                # Vérification du titre
                while True:
                    titre = input(f"Nouveau titre ({livre['titre']}) : ").strip()
                    if not titre:  # Garder l'ancien titre si l'entrée est vide
                        break
                    if len(titre) >= 3 and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", titre):
                        livre["titre"] = titre
                        break
                    print(
                        "❌ Le titre doit contenir au moins 3 lettres et ne pas inclure de chiffres ou caractères spéciaux.")

                # Vérification de l'auteur
                while True:
                    auteur = input(f"Nouvel auteur ({livre['auteur']}) : ").strip()
                    if not auteur:
                        break
                    if len(auteur) >= 3 and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", auteur):
                        livre["auteur"] = auteur
                        break
                    print(
                        "❌ Le nom de l'auteur doit contenir au moins 3 lettres et ne pas inclure de chiffres ou caractères spéciaux.")

                # Vérification du genre
                genres_valides = ["Roman", "Science-Fiction", "Policier", "Fantastique", "Histoire", "Biographie"]
                while True:
                    print("Genres disponibles :")
                    for genre in genres_valides:
                        print(f"- {genre}")
                    genre = input(f"Nouveau genre ({livre['genre']}) : ").strip()
                    if not genre:
                        break
                    if genre in genres_valides:
                        livre["genre"] = genre
                        break
                    print("❌ Genre invalide. Veuillez choisir un genre dans la liste.")

                # Vérification de l'année
                annee_actuelle = datetime.datetime.now().year
                while True:
                    annee = input(f"Nouvelle année ({livre['annee']}) : ").strip()
                    if not annee:
                        break
                    if annee.isdigit() and 1500 <= int(annee) <= annee_actuelle:
                        livre["annee"] = annee
                        break
                    print(f"❌ L'année doit être un nombre entre 1500 et {annee_actuelle}.")

                self.fichier.sauvegarder(self.livres)
                print("✅ Livre modifié avec succès!")
                return

        print("❌ Livre non trouvé!")

    def menu_livres(self):
        while True:
            print("\n📖 GESTION DES LIVRES 📖")
            print("1. Ajouter un livre")
            print("2. Afficher les livres")
            print("3. Modifier un livre")
            print("4. Supprimer un livre")
            print("5. Rechercher un livre")
            print("6. Retour")
            choix = input("Votre choix: ")

            if choix == "1":
                self.ajouter_livre()
            elif choix == "2":
                self.afficher_livres()
            elif choix == "3":
                self.modifier_livre()
            elif choix == "4":
                self.supprimer_livre()
            elif choix == "5":
                self.rechercher_livre()
            elif choix == "6":
                break
            else:
                print("❌ Choix invalide.")
