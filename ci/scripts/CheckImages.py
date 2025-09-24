import os
from PIL import Image

# ========================== #
# ==== Global variables ==== #
# ========================== #
MAX_SIZE_MB = 2.0
CONVERSION_QUALITY = 65
STATIC_LOCATION = "static"

# ============================== #
# ==== Recherche des images ==== #
# ============================== #
def GetImages(dossierPath):
    """
    Permet de parcourir le dossier statique pour trouver toutes les images

    Args :
        dossierPath : le chemin du dossier à parcourir

    Returns :
        list : la liste des chemins complets des images trouvées
    """
    images = []

    # Extensions d'images
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

    # On parcourt tous les directory et fichiers enfants
    for racine, dirs, fichiers in os.walk(dossierPath):
        for fichier in fichiers:

            # On vérifie si le fichier a une extension d'image
            _, ext = os.path.splitext(fichier.lower())
            if ext in image_extensions:
                images.append(os.path.join(racine, fichier))
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
        # On récupère la taille en bytes et on convertit en Mb
        SizeBytes = os.path.getsize(imagePath)
        SizeMb = SizeBytes / (1024 * 1024)
        return SizeMb, SizeMb > MAX_SIZE_MB
    
    except Exception as error:
        print(f"Error : problème de lecture de taille pour {imagePath} : {error}")
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

    # On vérifie si le dossier static existe
    if not os.path.exists(STATIC_LOCATION):
        print(f"Error :'{STATIC_LOCATION}' n'existe pas")
        exit(1)
    
    # On récupère toutes les images du dossier static
    allImages = GetImages(STATIC_LOCATION)
    
    if not allImages:
        print(f"Aucune image trouvée dans '{STATIC_LOCATION}'")
        exit(0)

    nbImagesTotal = len(allImages)
    nbImagesTraitees = 0

    print(f"Analyse de {nbImagesTotal} images dans '{STATIC_LOCATION}'...")

    # On vérifie chaque image et convertit si trop lourde
    for imagePath in allImages:
        nbImagesTraitees += 1

        tailleMb, isHeavy = CheckImageSize(imagePath)

        # Si l'image est trop lourde
        if isHeavy:
            webpPath = ConvertToWebP(imagePath, True)

            if webpPath:
                # Conversion réussie
                print(f"[{nbImagesTraitees}/{nbImagesTotal}] CONVERTED : '{imagePath}' ({tailleMb:.2f} MB) -> '{webpPath}'")
            else:
                # Erreur de conversion
                print(f"[{nbImagesTraitees}/{nbImagesTotal}] ERROR CONVERSION : '{imagePath}' ({tailleMb:.2f} MB)")
        else:
            # Taille OK
            print(f"[{nbImagesTraitees}/{nbImagesTotal}] OK : '{imagePath}' ({tailleMb:.2f} MB)")

    print("Analyse terminée.")