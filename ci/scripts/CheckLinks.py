import os
import re
from urllib import request


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


# ============================== #
# ==== Extraction des liens ==== #
# ============================== #
def GetLinks(fichierPath):
    """
    Permet de trouver tous les liens présents dans un fichier markdown

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

# ========================================= #
# ==== Vérification des liens internes ==== #
# ========================================= #
def InternalVerification(lien):
    """
    Permet de vérifier si un lien vers un fichier interne existe bien

    Args :
        lien : le chemin relatif à vérifier

    Returns :
        bool : True si le fichier existe sinon False
    """

    return os.path.exists(lien)

# ========================================= #
# ==== Vérification des liens externes ==== #
# ========================================= #
def ExternalVerification(url):
    """
    Permet de vérifier si un lien externe est accessible
    Dans ce contexte la un lien est un URL

    Args :
        url : l'URL à tester

    Returns :
        bool : True si l'URL répond sinon False
    """
    try:
        # On essaye d'abord une requête HEAD pour économe du temps et du bandwidth
        req = request.Request(url, method="HEAD")
        with request.urlopen(req, timeout=5) as response:
            if response.status < 400:
                return True
    except Exception:
        try:
            # Sinon requête GET
            with request.urlopen(url, timeout=5) as response:
                return response.status < 400
        except Exception:
            return False
    return False
    
if __name__ == "__main__":

    # On récupère tous les fichiers markdown
    allMd = FindAllMarkdown(".")

    # On récupère tous les liens
    allLiens = []
    for md in allMd:
        allLiens.extend(GetLinks(md))

    # Nombre total de liens
    nbLiensTotal = len(allLiens)
    nbLiensTraites = 0

    # On vérifie chaque lien
    for url, _ in allLiens:
        nbLiensTraites += 1

        # Affiche 1 si le lien fonctionne sinon 0
        if url.startswith("http"):
            print(f"{1 if ExternalVerification(url) else 0} {url} [{nbLiensTraites}/{nbLiensTotal}]")
        else:
            print(f"{1 if InternalVerification(url) else 0} {url} [{nbLiensTraites}/{nbLiensTotal}]")