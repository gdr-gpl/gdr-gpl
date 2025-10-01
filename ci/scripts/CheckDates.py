import os
import re
from datetime import datetime

# Title : Ficher permettant de verifier si toutes les dates sont au bon format


def getDate(dossierPath):
    fichier_md = FindAllMarkdown(dossierPath)
    erreurs = [] 
    erreur_trouvee = False

    for each_file in fichier_md:
        try:
            with open(each_file, 'r', encoding='utf-8') as f:
                date_found = False
                for i in range(10):
                    line = f.readline()
                    if not line:
                        break
                    date_trouvee = re.search(r'^date:\s*"?(.+?)"?$', line.strip())
                    if date_trouvee:
                        date_return = date_trouvee.group(1).strip()
                        try:
                            date_ = datetime.strptime(date_return, "%Y-%m-%dT%H:%M:%SZ")
                            if date_ > datetime.now():
                                erreurs.append(f"[{each_file}]  Date dans le futur : {date_return}")
                                erreur_trouvee = True
                            date_found = True
                            break
                        except ValueError:
                            erreurs.append(f"[{each_file}]  Format invalide : {date_return}")
                            erreur_trouvee = True
                            date_found = True
                            break
                if not date_found:
                    erreurs.append(f"[{each_file}]  Aucune date trouvée")
                    erreur_trouvee = True
        except FileNotFoundError:
            erreurs.append(f"[{each_file}]  Fichier introuvable")
            erreur_trouvee = True

    if erreurs:
        print(" Erreurs détectées ")
        for erreur in erreurs:
            print(erreur)
    else:
        print("Aucune erreur détectée.")

    return 1 if erreur_trouvee else 0


# ================================ #
# ==== Recherche des fichiers ==== #
# ================================ #
def FindAllMarkdown(dossierPath):
    """
    Permet de parcourir le dossier donné de manière recursive pour trouver tous les fichiers markdown

    Args :
        dossier/ :  le chemin du dossier à parcourir

    Returns :
        list : la liste des chemins complets des fichiers Markdown trouvés
    """
    markdowns = []


    # On parcourt tous les directory et fichiers enfants
    for racine, dirs, fichiers in os.walk(dossierPath):
        for fichier in fichiers:

            # Si le fichier se termine par un .md alors on l'ajoute à la liste
            if fichier.endswith('.md'):
                markdowns.append(os.path.join(racine, fichier))
    return markdowns


def run():
    result = getDate("content/")
    print("Code de retour :", result)
    return result


if __name__ == "__main__":
    run()
