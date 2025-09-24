import os
import re
import glob
from pathlib import Path

def main():
    # Obtenir tous les fichiers .md dans le dossier content et ses sous-dossiers
    content_path = "../content"
    if not os.path.exists(content_path):
        print(f"Erreur: Le dossier '{content_path}' n'existe pas")
        return
    
    # Rechercher tous les fichiers .md récursivement
    md_files = glob.glob(os.path.join(content_path, "**", "*.md"), recursive=True)
    
    total_urls = 0
    # Regex pour capturer les URLs vers des pages web (pas les PDFs ou autres fichiers)
    # Capture les liens http/https vers gdr-gpl.cnrs.fr qui ne se terminent pas par des extensions de fichiers
    url_pattern = r'https?://gdr-gpl\.cnrs\.fr(?!.*\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|tar|gz|jpg|jpeg|png|gif|svg|mp4|avi|mov))'
    
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if re.search(url_pattern, content):
            print(f"Fichier avec urls GDR: {file_path}")
            total_urls += 1

    print(f"Nombre total d'URLs GDR trouvées: {total_urls}")

if __name__ == "__main__":
    main()