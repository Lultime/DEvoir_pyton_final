from livre import LivreManager
from utlisateur import UtilisateurManager
from emprunt_livre import EmpruntManager
from statistique import afficher_statistiques

def afficher_menu():
    livres = LivreManager()
    utilisateurs = UtilisateurManager()
    emprunts = EmpruntManager()

    while True:
        print("\n📚 MENU PRINCIPAL 📚")
        print("1. Gestion des livres")
        print("2. Gestion des utilisateurs")
        print("3. Gestion des emprunts")
        print("4. Statistiques")
        print("5. Quitter")
        choix = input("Entrez votre choix: ")

        if choix == "1":
            livres.menu_livres()
        elif choix == "2":
            utilisateurs.menu_utilisateurs()
        elif choix == "3":
            emprunts.menu_emprunts()
        elif choix == "4":
            afficher_statistiques()
        elif choix == "5":
            print("✅ Au revoir!")
            break
        else:
            print("❌ Choix invalide.")

if __name__ == "__main__":
    afficher_menu()
