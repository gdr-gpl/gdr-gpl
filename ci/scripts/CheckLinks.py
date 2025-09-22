import os
import re


# ================================ #
# ==== Recherche des fichiers ==== #
# ================================ #
def FindAllMarkdown(dossierPath):
    """
    Parcourt le dossier donné de manière recursive pour trouver tous les fichiers markdown

    Args :
        dossier/ :  le chemin du dossier à parcourir

    Returns :
        list : la liste des chemins complets des fichiers Markdown trouvés
    """
    markdowns = []

    # On parcourt tous les directory et fichiers enfants
    for racine, fichiers in os.walk(dossierPath):
        for fichier in fichiers:

            # Si le fichier se termine par un .md alors on l'ajoute à la liste
            if fichier.endswith('.md'):
                markdowns.append(os.path.join(racine, fichier))
    return markdowns


# ============================== #
# ==== Extraction des liens ==== #
# ============================== #
def GetLinks(fichierPath):
    """
    Trouve tous les liens présents dans un fichier markdown

    Args :
        fichierPath : le path du fichier à analyser

    Returns :
        list : la liste des tuples url, texte_affichage
    """
    
    liens = []
    try:

        # On ouvre le fichier en mode lecture
        with open(fichierPath, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()

        # On cherche les liens markdown
        # Type : [texte](url)
        markdownLinks = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', contenu)

        # On cherche les liens href 
        # Type : <a href="url">
        htmlLinks = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', contenu)

        # On cherche les liens classique
        # Type : https://...
        urlLinks = re.findall(r'<(https?://[^>]+)>', contenu)

        # On ajoute chaque lien à la liste
        for texte, url in markdownLinks:
            liens.append((url, f"[{texte}]({url})"))
        for url in htmlLinks:
            liens.append((url, f'href="{url}"'))
        for url in urlLinks:
            liens.append((url, f"<{url}>"))

    except Exception as error:
        print(f"Error : problème de lecture dans {fichierPath} : {error}")

    return liens