#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
from pathlib import Path

def convert_date_format(old_date_string):
    """
    Convertit les dates du format ancien au nouveau format
    Format ancien: Thu, 05 Dec 2024 17:10:56 +0000
    Format nouveau: "2024-12-05T17:10:56Z"
    """
    
    # Mapping des mois en anglais vers numéros
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    
    # Pattern regex pour parser la date
    pattern = r'([A-Z][a-z]{2}), (\d{2}) ([A-Z][a-z]{2}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) \+0000'
    
    match = re.match(pattern, old_date_string)
    if match:
        day = match.group(2)
        month = month_map.get(match.group(3), '01')
        year = match.group(4)
        hour = match.group(5)
        minute = match.group(6)
        second = match.group(7)
        
        return f'"{year}-{month}-{day}T{hour}:{minute}:{second}Z"'
    
    return old_date_string

def main():
    # Obtenir tous les fichiers .md dans le dossier content et ses sous-dossiers
    content_path = "content/posts"
    if not os.path.exists(content_path):
        print(f"Erreur: Le dossier '{content_path}' n'existe pas")
        return
    
    # Rechercher tous les fichiers .md récursivement
    md_files = glob.glob(os.path.join(content_path, "**", "*.md"), recursive=True)
    
    url_file = "attachment_urls.txt"
    
    total_files = 0
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
            
            # Vérifier si le fichier contient des dates à convertir
            if re.search(url_pattern, content):
                total_files += 1
                print(f"Traitement du fichier: {file_path}")
                print(re.search(url_pattern, content).group(0))
                
            #     # Fonction de remplacement pour les dates
            #     def replace_date(match):
            #         old_date = match.group(1)
            #         new_date = convert_date_format(old_date)
            #         return f"date: {new_date}"
                
            #     # Remplacer toutes les occurrences de dates dans ce fichier
            #     content = re.sub(date_pattern, replace_date, content)
                
            #     # Écrire le contenu modifié dans le fichier si des changements ont été faits
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
    print(f"Fichiers traités: {converted_files} sur {total_files} fichiers avec des dates à convertir")

if __name__ == "__main__":
    main()