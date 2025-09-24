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

# ===================================== #
# ==== Vérification de l'existence ==== #
# ===================================== #
def ImageExists(imagePath):
    """
    Permet de vérifier si une image existe bien

    Args :
        imagePath : le chemin de l'image à vérifier

    Returns :
        bool : True si l'image existe sinon False
    """
    # On ignore les liens externes
    if imagePath.startswith("http"):
        return True
        
    return os.path.exists(imagePath)

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

# =============================== #
# ==== Conversion des images ==== #
# =============================== #
def ConvertToWebP(imagePath, deleteOldFile=False):
    """
    Permet de convertir une image au format WebP et supprimer l'ancien fichier si demandé

    Args :
        imagePath : le chemin de l'image à convertir
        deleteOldFile : bool qui supprime l'ancien fichier si True

    Returns :
        str : le chemin de l'image convertie
    """
    try:
        if not os.path.exists(imagePath):
            return None

        with Image.open(imagePath) as img:
            webpPath = os.path.splitext(imagePath)[0] + '.webp'
            img.save(webpPath, 'WebP', quality=CONVERSION_QUALITY, optimize=True)

        if deleteOldFile and os.path.exists(webpPath):
            try:
                os.remove(imagePath)
            except Exception as error:
                print(f"Error : problème de suppression avec {imagePath} : {error}")

        return webpPath

    except Exception as error:
        print(f"Error : probl-me de conversion avec {imagePath} : {error}")
        return None
    

if __name__ == "__main__":
    
    # On récupère tous les fichiers markdown
    allMd = FindAllMarkdown(".")

    # On récupère toutes les images
    allImages = []
    for md in allMd:
        allImages.extend(GetImages(md))

    nbImagesTotal = len(allImages)
    nbImagesTraitees = 0

    # On vérifie chaque image et convertit si trop lourde
    for imagePath in allImages:
        nbImagesTraitees += 1

        # Vérifie si l'image existe
        if ImageExists(imagePath):
            tailleMb, isHeavy = CheckImageSize(imagePath)

            # Si l'image trop lourde + pas un lien externe
            if isHeavy and not imagePath.startswith("http"):
                webpPath = ConvertToWebP(imagePath, True)

                if webpPath:

                    # Conversion réussie
                    print(f"[{nbImagesTraitees}/{nbImagesTotal}] CONVERTED : '{imagePath}' ({tailleMb:.2f} MB) -> '{webpPath}'")
                else:

                    # Conversion error
                    print(f"[{nbImagesTraitees}/{nbImagesTotal}] ERROR CONVERSION : '{imagePath}' ({tailleMb:.2f} MB)")
            else:

                # Taille OK
                print(f"[{nbImagesTraitees}/{nbImagesTotal}] OK : '{imagePath}' ({tailleMb:.2f} MB) - OK")
        else:

            # Non trouvée
            print(f"[{nbImagesTraitees}/{nbImagesTotal}] NOT FOUND : '{imagePath}'")