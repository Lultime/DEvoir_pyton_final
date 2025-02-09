import json
import random
from emprunt_manager import FichierManager
import re

class Utilisateur:
    def __init__(self, nom, prenom, email):
        self.__id = "UT" + str(random.randint(1000, 9999))
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email

    # Getters
    def get_id(self):
        return self.__id

    def get_nom(self):
        return self.__nom

    def get_prenom(self):
        return self.__prenom

    def get_email(self):
        return self.__email

    # Setters
    def set_nom(self, nom):
        self.__nom = nom

    def set_prenom(self, prenom):
        self.__prenom = prenom

    def set_email(self, email):
        self.__email = email

    def to_dict(self):
        return {"id": self.__id, "nom": self.__nom, "prenom": self.__prenom, "email": self.__email}


class UtilisateurManager:
    def __init__(self):
        self.fichier = FichierManager("utilisateur.json")
        self.utilisateurs = self.fichier.charger()



    def ajouter_utilisateur(self):
        # Vérification du nom
        while True:
            nom = input("Nom: ")
            if re.match(r"^[a-zA-Zà-ÿÀ-Ÿ\- ]+$",
                        nom):  # Vérifie que le nom ne contient que des lettres, espaces et tirets
                break
            print("❌ Nom invalide. Le nom ne doit contenir que des lettres, des espaces ou des tirets.")

        # Vérification du prénom
        while True:
            prenom = input("Prénom: ")
            if re.match(r"^[a-zA-Zà-ÿÀ-Ÿ\- ]+$",
                        prenom):  # Vérifie que le prénom ne contient que des lettres, espaces et tirets
                break
            print("❌ Prénom invalide. Le prénom ne doit contenir que des lettres, des espaces ou des tirets.")

        # Vérification de l'email
        while True:
            email = input("Email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Vérifie si l'email contient "@" et un domaine valide
                break
            print("❌ Email invalide. Veuillez entrer un email valide.")

        utilisateur = Utilisateur(nom, prenom, email)
        self.utilisateurs.append(utilisateur.to_dict())
        self.fichier.sauvegarder(self.utilisateurs)
        print(f"✅ Utilisateur ajouté avec ID {utilisateur.get_id()}")

    def afficher_utilisateurs(self):
        if not self.utilisateurs:
            print("👤 Aucun utilisateur enregistré.")
            return

        for utilisateur in self.utilisateurs:
            print(f"ID : {utilisateur['id']}")
            print(f"Nom : {utilisateur['nom']} {utilisateur['prenom']}")
            print(f"Email : {utilisateur['email']}")
            print("-" * 30)  # Séparateur pour plus de lisibilité

    def supprimer_utilisateur(self):
        self.afficher_utilisateurs()
        id_utilisateur = input("ID de l'utilisateur à supprimer: ")
        self.utilisateurs = [u for u in self.utilisateurs if u["id"] != id_utilisateur]
        self.fichier.sauvegarder(self.utilisateurs)
        print("✅ Utilisateur supprimé!")



    def modifier_utilisateur(self):
        self.afficher_utilisateurs()
        id_utilisateur = input("ID de l'utilisateur à modifier: ")

        for utilisateur in self.utilisateurs:
            if utilisateur["id"] == id_utilisateur:
                # Vérification du nom
                while True:
                    nouveau_nom = input(f"Nouveau nom ({utilisateur['nom']}): ").strip()
                    if not nouveau_nom:  # Si l'utilisateur ne saisit rien, on garde l'ancien nom
                        break
                    if re.match(r"^[a-zA-Zà-ÿÀ-Ÿ\- ]+$", nouveau_nom):
                        utilisateur["nom"] = nouveau_nom
                        break
                    print("❌ Nom invalide. Il ne doit contenir que des lettres, des espaces ou des tirets.")

                # Vérification du prénom
                while True:
                    nouveau_prenom = input(f"Nouveau prénom ({utilisateur['prenom']}): ").strip()
                    if not nouveau_prenom:  # Si l'utilisateur ne saisit rien, on garde l'ancien prénom
                        break
                    if re.match(r"^[a-zA-Zà-ÿÀ-Ÿ\- ]+$", nouveau_prenom):
                        utilisateur["prenom"] = nouveau_prenom
                        break
                    print("❌ Prénom invalide. Il ne doit contenir que des lettres, des espaces ou des tirets.")

                # Vérification de l'email
                while True:
                    nouveau_email = input(f"Nouveau email ({utilisateur['email']}): ").strip()
                    if not nouveau_email:  # Si l'utilisateur ne saisit rien, on garde l'ancien email
                        break
                    if re.match(r"[^@]+@[^@]+\.[^@]+", nouveau_email):
                        utilisateur["email"] = nouveau_email
                        break
                    print("❌ Email invalide. Veuillez entrer un email valide.")

                # Sauvegarde des modifications
                self.fichier.sauvegarder(self.utilisateurs)
                print("✅ Utilisateur modifié avec succès!")
                return

        print("❌ Utilisateur non trouvé!")

    def menu_utilisateurs(self):
        while True:
            print("\n👤 GESTION DES UTILISATEURS 👤")
            print("1. Ajouter un utilisateur")
            print("2. Afficher les utilisateurs")
            print("3. Modifier un utilisateur")
            print("4. Supprimer un utilisateur")
            print("5. Retour")
            choix = input("Votre choix: ")

            if choix == "1":
                self.ajouter_utilisateur()
            elif choix == "2":
                self.afficher_utilisateurs()
            elif choix == "3":
                self.modifier_utilisateur()
            elif choix == "4":
                self.supprimer_utilisateur()
            elif choix == "5":
                break
            else:
                print("❌ Choix invalide.")
