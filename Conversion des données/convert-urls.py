#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
from pathlib import Path



def convertUrlToRelative(url):
    """
    Convertit une URL absolue en URL relative si elle est trouvée dans le contenu des URLs.
    """
    mediaName = url.split('/')[-1]
    folderName = mediaName.split('.')[-1]
    alt = mediaName.split('.')[0]
    # Créer le dossier s'il n'existe pas
    # os.makedirs(f"/assets/{folderName}", exist_ok=True)
    relativeUrl = f"/assets/{folderName}/{mediaName}"
    imgTag = f'img src="{relativeUrl}" alt="{alt}"/'
    return imgTag

def main():
    # Obtenir tous les fichiers .md dans le dossier content et ses sous-dossiers
    content_path = "../content"
    if not os.path.exists(content_path):
        print(f"Erreur: Le dossier '{content_path}' n'existe pas")
        return
    
    # Rechercher tous les fichiers .md récursivement
    md_files = glob.glob(os.path.join(content_path, "**", "*.md"), recursive=True)
    
    url_file = "attachment_urls.txt"
    
    if not os.path.exists(url_file):
        print(f"Erreur: Le fichier '{url_file}' n'existe pas")
        return
    with open(url_file, 'r', encoding='utf-8') as f:
        url_content = f.read()
    
    total_urls = 0
    converted_files = 0
    
    # Pattern pour détecter les URLs
    url_pattern = r'https?://[^\s\)]+\.(jpe?g|png|gif|pdf|pptx|docx|doc|zip|JPE?G|PNG|GIF|PDF)'
    
    # Pattern pour détecter les dates à convertir
    date_pattern = r'date: ([A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2} \+0000)'
    
    print(f"Début du traitement des fichiers markdown...")
    print(f"Nombre de fichiers trouvés: {len(md_files)}")
    
    for file_path in md_files:
        try:
            # Lire le contenu du fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content

            if(file_path.startswith("content/attachments") or file_path.startswith("content/toutesInfos")):
                continue
            
            # Vérifier si le fichier contient des urls à convertir
            if re.search(url_pattern, content): 
                
                print(f"Traitement du fichier: {file_path}")
                # Trouver et convertir toutes les URLs dans le contenu
                for url in re.finditer(url_pattern, content):
                    url = url.group(0)
                    relativeUrl = convertUrlToRelative(url)
                    content = re.sub(url, relativeUrl, content)
                    total_urls += 1
                    
                # Écrire le contenu modifié dans le fichier si des changements ont été faits
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    converted_files += 1
                    print(f"Converti: {file_path}")
                
                
            #     # Fonction de remplacement pour les dates
            #     def replace_date(match):
            #         old_date = match.group(1)
            #         new_date = convert_date_format(old_date)
            #         return f"date: {new_date}"
                
            #     # Remplacer toutes les occurrences de dates dans ce fichier
            #     content = re.sub(date_pattern, replace_date, content)
                
            #     if content != original_content:
            #         with open(file_path, 'w', encoding='utf-8') as f:
            #             f.write(content)
            #         converted_files += 1
            #         print(f"Converti: {file_path}")
            
            # # Optionnel: Vérifier et traiter les URLs si nécessaire
            # if re.search(url_pattern, content):
            #     # Exemple de remplacement d'URLs absolues par relatives
            #     # content = re.sub(r'https://gdr-gpl\.cnrs\.fr/wp-content/uploads/', '/uploads/', content)
            #     pass
                
        except Exception as e:
            print(f"Erreur lors du traitement de {file_path}: {e}")
    
    print("Conversion terminée!")
    print(f"Urls traités: {total_urls} sur {converted_files} fichiers avec des urls converties.")

if __name__ == "__main__":
    main()
    
    
# {{< link title="hjfhf"> }}