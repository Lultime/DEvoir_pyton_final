from livre import LivreManager
from utlisateur import UtilisateurManager
from emprunt_livre import EmpruntManager

def afficher_statistiques():
    livres = LivreManager().fichier.charger()
    utilisateurs = UtilisateurManager().fichier.charger()
    emprunts = EmpruntManager().fichier.charger()

    print("\n📊 STATISTIQUES 📊")
    print(f"📚 Nombre total de livres : {len(livres)}")
    print(f"👤 Nombre total d'utilisateurs : {len(utilisateurs)}")
    print(f"📌 Nombre total d'emprunts : {len(emprunts)}")
