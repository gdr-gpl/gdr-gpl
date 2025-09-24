import os
import re
from PIL import Image

# ========================== #
# ==== Global variables ==== #
# ========================== #
MAX_SIZE_MB = 2.0
CONVERSION_QUALITY = 75

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

# ======================== #
# ==== Get des images ==== #
# ======================== #
def GetImages(fichierPath):
    """
    Permet de trouver toutes les images dans un ifhcier markdown

    Args :
        fichierPath : le path du fichier à analyser

    Returns :
        list : la liste des chemins d'images trouvés
    """
    images = []
    
    try:
        # On ouvre le fichier en mode lecture
        with open(fichierPath, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()

        # On cherche les images markdown
        # Type : ![alt](image.jpg)
        markdownImages = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', contenu)

        # On cherche les images HTML
        # Type : <img src="image.jpg">
        htmlImages = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', contenu)

        # On ajoute toutes les images trouvées
        images.extend(markdownImages)
        images.extend(htmlImages)

    except Exception as error:
        print(f"Error : problème de lecture dans {fichierPath} : {error}")

    return images

# ================================ #
# ==== Vérification de taille ==== #
# ================================ #
def CheckImageSize(imagePath):
    """
    Permet de vérifier si une image est trop lourde

    Args :
        imagePath : le chemin de l'image à vérifier

    Returns :
        tuple : (taille_en_MB, est_trop_lourde)
    """
    try:
        if os.path.exists(imagePath):

            # On récupère la taille en bytes et on convertit en Mb
            SizeBytes = os.path.getsize(imagePath)
            SizeMb = SizeBytes / (1024 * 1024)
            return SizeMb, SizeMb > MAX_SIZE_MB
    except Exception:
        pass
    
    return 0, False
