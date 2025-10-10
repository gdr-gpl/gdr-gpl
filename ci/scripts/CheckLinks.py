import os
import re
import json
from urllib import request
from urllib.parse import urlparse

# Title : Fichier permettant de vérifier les liens dans les fichiers markdown

# Variables globales
# Si True on vérifie seulement les domaines des URLs externes
FAST_CHECK = True

# Cache des domaines déjà testés en mode FAST_CHECK
domain_cache = {}

# ======================================== #
# ==== Récupération des liens ignorés ==== #
# ======================================== #
def GetIgnoredLinks():
    """
    Récupère la liste des liens à ignorer dans le fichier ignoredlinks.json
    
    Returns :
        list : la liste des liens à ignorer
    """
    try:
        with open('.\\ci\\scripts\\ignoredlinks.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

ignored_links = GetIgnoredLinks()

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

    # Si le lien est un anchor link, lien relatif ou address mail il est automatiquement validé
    if lien.startswith('#') or '@' in lien or '?' in lien or lien in ignored_links:
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

# ================================= #
# ==== Récupération du domaine ==== #
# ================================= #
def GetDomainOnly(url):
    """
    Récupère le domaine d'un URL (par exemple https://github.com)

    Args :
        url : l'URL complète

    Returns :
        str : le domaine principal
    """
    try:

        pathlessURL = urlparse(url)
        
        # partie https
        scheme = pathlessURL.scheme

        # partie github.com
        netloc = pathlessURL.netloc
        
        return f"{scheme}://{netloc}"

    except Exception:
        return url

# ========================================= #
# ==== Vérification des liens externes ==== #
# ========================================= #
def ExternalVerification(url):
    """
    Permet de vérifier si un lien externe est accessible

    Args :
        url : l'URL à tester

    Returns :
        bool : True si l'URL répond sinon False
    """
    
    global domain_cache

    # Si ignore link n'est pas vide ou Fast Check est activé alors on récupère le domaine
    if ignored_links or FAST_CHECK:
        domain = GetDomainOnly(url)

    #### Si le domaine est dans la liste des liens ignorés il est automatiquement validé ####
    if ignored_links and (domain in ignored_links):
        return True
    
    # Si FAST_CHECK est activé
    if FAST_CHECK:
        try:
            
            # Si le domaine est déjà dans le cache on retourne le résultat mis en cache
            if domain in domain_cache:
                return domain_cache[domain]
            
            # Sinon on teste le domaine et on le met en cache
            result = TestDomain(domain)
            domain_cache[domain] = result
            return result
            
        except Exception:
            pass
    else:
        # Sinon on teste l'URL complète
        return TestFullUrl(url)

def TestDomain(domain):
    """
    Test si un domaine est accessible (sans le path, par exemple https://google.com et pas https://google.com/search etc)

    Args :
        domain : l'URL du domaine à tester

    Returns :
        bool : True si le domaine répond sinon False
    """
    try:
        # On essaye d'abord une requête HEAD pour économe du temps et du bandwidth
        req = request.Request(domain, method="HEAD")

        with request.urlopen(req, timeout=5) as response:
            if response.status < 400:
                return True
            
    except Exception:
        try:

            # Sinon requête GET
            with request.urlopen(domain, timeout=5) as response:
                return response.status < 400
        except Exception:
            return False
    return False

def TestFullUrl(url):
    """
    Test si un URL full est accessible

    Args :
        url : l'URL full à tester

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
    

def run():


    # On récupère tous les fichiers markdown
    allMd = FindAllMarkdown(".")


    erreurs = False;

    # On récupère tous les liens
    allLiens = []
    for md in allMd:
        allLiens.extend(GetLinks(md))

    # Nombre total de liens
    nbLiensTotal = len(allLiens)
    nbLiensTraites = 0

    print(f"Mode de vérification : {'FAST_CHECK (domaines seulement)' if FAST_CHECK else 'COMPLET (chaque URL)'}")

    # On vérifie chaque lien
    for url, display_text, source_file in allLiens:
        nbLiensTraites += 1

        # Affiche ✓ si le lien fonctionne sinon X
        if url.startswith("http"):
            result = ExternalVerification(url)
            cacheInfo = ""
            if FAST_CHECK:
                try:
                    pathlessURL = urlparse(url)
                    scheme = pathlessURL.scheme
                    netloc = pathlessURL.netloc
                    domain = f"{scheme}://{netloc}"

                    cacheInfo = " (cached)" if domain in domain_cache and nbLiensTraites > 1 else " (nouveau domaine)"
                except:
                    pass
            print(f"{'✓' if result else 'X'} [{nbLiensTraites}/{nbLiensTotal}] {url}{cacheInfo}")

        else:
            result = InternalVerification(url, source_file)
            print(f"{'✓' if result else 'X'} [{nbLiensTraites}/{nbLiensTotal}] {url}")

