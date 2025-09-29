#!/bin/bash

# Script pour extraire les URLs d'attachement des fichiers .md
echo "Début de l'extraction des URLs d'attachement..."

# Initialiser le fichier de sortie
output_file="attachment_urls.txt"
> "$output_file"

# Compter les fichiers trouvés
file_count=$(find "content/toutesInfos/attachment" -name "*.md" | wc -l)
echo "Nombre de fichiers trouvés: $file_count"

# Itérer sur tous les fichiers .md dans le dossier
find "content/toutesInfos/attachment" -name "*.md" | while read -r file; do
    # Extraire l'URL d'attachement du fichier
    attachment_url=$(grep "^attachment_url:" "$file" | sed 's/attachment_url: *//')
    
    if [ -n "$attachment_url" ]; then
        # Ajouter l'URL au fichier de sortie
        echo "$attachment_url" >> "$output_file"
        echo "URL extraite de $(basename "$file"): $attachment_url"
    else
        echo "Aucune URL d'attachement trouvée dans $(basename "$file")"
    fi
done

echo "Extraction terminée. Les URLs ont été sauvegardées dans $output_file"