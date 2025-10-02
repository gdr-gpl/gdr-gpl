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
        
    print(f"Début du traitement des fichiers markdown...")
    print(f"Nombre de fichiers trouvés: {len(md_files)}")
    
    for file_path in md_files:
        try:
            # Lire le contenu du fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
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
                
                
        except Exception as e:
            print(f"Erreur lors du traitement de {file_path}: {e}")
    
    print("Conversion terminée!")
    print(f"Urls traités: {total_urls} sur {converted_files} fichiers avec des urls converties.")

if __name__ == "__main__":
    main()
    
    
# {{< link title="hjfhf"> }}