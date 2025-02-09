import json
import os


class FichierManager:
    def __init__(self, fichier):
        self.fichier = fichier

    def charger(self):

        if not os.path.exists(self.fichier):
            return []  # Retourne une liste vide si le fichier n'existe pas

        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                contenu = f.read().strip()  # Lire et supprimer les espaces inutiles
                if not contenu:
                    return []  # Si le fichier est vide, retourner une liste vide
                return json.loads(contenu)  # Charger le JSON
        except (json.JSONDecodeError, FileNotFoundError):
            print(f" Erreur : {self.fichier} est vide ")
            self.sauvegarder([])  # Réinitialiser le fichier
            return []  # Retourner une liste vide

    def sauvegarder(self, data):

        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
