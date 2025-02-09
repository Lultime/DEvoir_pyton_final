import json
import random
from emprunt_manager import FichierManager
from livre import LivreManager
from utlisateur import UtilisateurManager
from datetime import datetime
import re
from datetime import datetime

class Emprunt:
    def __init__(self, id_livre, id_utilisateur, date_emprunt, date_retour):
        self.__id = "EM" + str(random.randint(1000, 9999))
        self.__id_livre = id_livre
        self.__id_utilisateur = id_utilisateur
        self.__date_emprunt = date_emprunt
        self.__date_retour = date_retour

    # Getters
    def get_id(self):
        return self.__id

    def get_id_livre(self):
        return self.__id_livre

    def get_id_utilisateur(self):
        return self.__id_utilisateur

    def get_date_emprunt(self):
        return self.__date_emprunt

    def get_date_retour(self):
        return self.__date_retour

    # Setters
    def set_date_retour(self, date_retour):
        self.__date_retour = date_retour


# __ pour rendre ma variable prive
    def to_dict(self):
        return {
            "id": self.__id,
            "id_livre": self.__id_livre,
            "id_utilisateur": self.__id_utilisateur,
            "date_emprunt": self.__date_emprunt,
            "date_retour": self.__date_retour
        }


class EmpruntManager:
    def __init__(self):
        self.fichier = FichierManager("emprunts.json")
        self.emprunts = self.fichier.charger()



    def emprunter_livre(self):
        livres = LivreManager()
        utilisateurs = UtilisateurManager()

        livres.afficher_livres()

        # Vérification de l'ID du livre
        while True:
            id_livre = input("ID du livre à emprunter: ").strip()
            if id_livre and any(livre["id"] == id_livre for livre in livres.livres):  # Vérifie si l'ID existe
                break
            print("❌ ID du livre invalide ou introuvable. Veuillez entrer un ID valide.")

        utilisateurs.afficher_utilisateurs()

        # Vérification de l'ID de l'utilisateur
        while True:
            id_utilisateur = input("ID de l'utilisateur: ").strip()
            if id_utilisateur and any(utilisateur["id"] == id_utilisateur for utilisateur in utilisateurs.utilisateurs):
                break
            print("❌ ID de l'utilisateur invalide ou introuvable. Veuillez entrer un ID valide.")

        # Vérification de la date d'emprunt
        while True:
            date_emprunt = input("Date d'emprunt (AAAA-MM-JJ): ").strip()
            if re.match(r"^\d{4}-\d{2}-\d{2}$", date_emprunt):  # Vérifie le format
                try:
                    date_emprunt_obj = datetime.strptime(date_emprunt, "%Y-%m-%d")
                    break
                except ValueError:
                    pass
            print("❌ Date d'emprunt invalide. Veuillez entrer une date au format AAAA-MM-JJ.")

        # Vérification de la date de retour
        while True:
            date_retour = input("Date de retour prévue (AAAA-MM-JJ): ").strip()
            if re.match(r"^\d{4}-\d{2}-\d{2}$", date_retour):  # Vérifie le format
                try:
                    date_retour_obj = datetime.strptime(date_retour, "%Y-%m-%d")
                    if date_retour_obj > date_emprunt_obj:  #  date de retour  après la date d'emprunt
                        break
                except ValueError:
                    pass
            print(
                "❌ Date de retour invalide. La date doit être au format AAAA-MM-JJ et postérieure à la date d'emprunt.")

        # Enregistrement de l'emprunt
        emprunt = Emprunt(id_livre, id_utilisateur, date_emprunt, date_retour)
        self.emprunts.append(emprunt.to_dict())
        self.fichier.sauvegarder(self.emprunts)
        print(f"✅ Emprunt enregistré avec ID {emprunt.get_id()}")

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
            print("-" * 30)  # Séparateur entre chaque livre

    def afficher_emprunts(self):
        if not self.emprunts:
            print("Aucun emprunt effectues.")
            return

        for emprunt in self.emprunts:
            print(f"ID : {emprunt['id']}")
            print(f"ID utilisateur : {emprunt['id_utilisateur']}")
            print(f"Date emprunt : {emprunt['date_emprunt']}")
            print(f"Date retour : {emprunt['date_retour']}")
            print("-" * 30)  # Séparateur entre chaque emprunt

    def retourner_livre(self):
        self.afficher_emprunts()
        id_emprunt = input("ID de l'emprunt à clôturer: ")

        emprunt_trouve = None
        for emprunt in self.emprunts:
            if emprunt["id"] == id_emprunt:
                emprunt_trouve = emprunt
                break

        if not emprunt_trouve:
            print("❌ Emprunt non trouvé.")
            return

        # Vérifier la date de retour
        date_retour = datetime.strptime(emprunt_trouve["date_retour"], "%Y-%m-%d")
        today = datetime.today()

        if today > date_retour:
            jours_retard = (today - date_retour).days
            penalite = jours_retard * 1  # Exemple : 1 unité par jour de retard
            print(f"⚠️ Retard de {jours_retard} jours. Pénalité de {penalite} unités à payer.")
        else:
            print("✅ Livre retourné à temps, aucune pénalité.")

        # Supprimer l'emprunt retourné
        self.emprunts = [e for e in self.emprunts if e["id"] != id_emprunt]
        self.fichier.sauvegarder(self.emprunts)

        print("📌 Livre bien retourné !")

    def modifier_emprunt(self):
        self.afficher_emprunts()
        id_emprunt = input("ID de l'emprunt à modifier: ")
        for emprunt in self.emprunts:
            if emprunt["id"] == id_emprunt:
                emprunt["date_retour"] = input(f"Nouvelle date de retour ({emprunt['date_retour']}): ") or emprunt[
                    "date_retour"]
                self.fichier.sauvegarder(self.emprunts)
                print("✅ Emprunt modifié avec succès!")
                return
        print("❌ Emprunt non trouvé!")

    def menu_emprunts(self):
        while True:
            print("\n📌 GESTION DES EMPRUNTS 📌")
            print("1. Enregistrer un emprunt")
            print("2. Afficher les emprunts")
            print("3. Modifier un emprunt")
            print("4. Retourner un livre")
            print("5. Retour")
            choix = input("Votre choix: ")

            if choix == "1":
                self.emprunter_livre()
            elif choix == "2":
                self.afficher_emprunts()
            elif choix == "3":
                self.modifier_emprunt()
            elif choix == "4":
                self.retourner_livre()
            elif choix == "5":
                break
            else:
                print("❌ Choix invalide.")
