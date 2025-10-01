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
        list : la liste des tuples (url, texte_affichage, fichier_source)
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

        # On ajoute chaque lien à la liste avec le fichier source
        for texte, url in markdownLinks:
            liens.append((url, f"[{texte}]({url})", fichierPath))
        for url in htmlLinks:
            liens.append((url, f'href="{url}"', fichierPath))
        for url in urlLinks:
            liens.append((url, f"<{url}>", fichierPath))

    except Exception as error:
        print(f"Error : problème de lecture dans {fichierPath} : {error}")

    return liens

# ========================================= #
# ==== Vérification des liens internes ==== #
# ========================================= #
def InternalVerification(lien, fichier_source):
    """
    Permet de vérifier si un lien vers un fichier interne existe bien

    Args :
        lien : le chemin relatif à vérifier
        fichier_source : le fichier markdown qui contient ce lien

    Returns :
        bool : True si le fichier existe sinon False
    """
    
    # Si le lien est un anchor link ou address mail il est automatiquement validé
    if lien.startswith('#') or '@' in lien:
        return True
    
    # Si le lien commence par /
    # il est relatif à la racine du projet
    if lien.startswith('/'):
        cheminAbsolu = lien[1:]
    else:

        # Sinon il est relatif au dossier du fichier source
        dossierSource = os.path.dirname(fichier_source)
        cheminAbsolu = os.path.join(dossierSource, lien)
    
    # On normalise le chemin pour résoudre les ../ et ./
    cheminAbsolu = os.path.normpath(cheminAbsolu)
    
    return os.path.exists(cheminAbsolu)

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
            with request.urlopen(url, timeout=15) as response:
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
    for url, display_text, source_file in allLiens:
        nbLiensTraites += 1

        # Affiche ✓ si le lien fonctionne sinon 0
        if url.startswith("http"):
            result = ExternalVerification(url)
            print(f"{'✓' if result else 'X'} [{nbLiensTraites}/{nbLiensTotal}] {url}")
        else:
            result = InternalVerification(url, source_file)
            print(f"{'✓' if result else 'X'} [{nbLiensTraites}/{nbLiensTotal}] {url}")