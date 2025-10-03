#!/bin/bash

# Script bash pour convertir les dates du format ancien au nouveau format
# Format ancien: Thu, 05 Dec 2024 17:10:56 +0000
# Format nouveau: "2024-12-05T17:10:56Z"

function convert_date() {
    local old_date="$1"
    
    # Associer les mois anglais aux numéros
    declare -A months=(
        ["Jan"]="01" ["Feb"]="02" ["Mar"]="03" ["Apr"]="04"
        ["May"]="05" ["Jun"]="06" ["Jul"]="07" ["Aug"]="08"
        ["Sep"]="09" ["Oct"]="10" ["Nov"]="11" ["Dec"]="12"
    )
    
    # Parser la date avec regex
    if [[ $old_date =~ ^[A-Z][a-z]{2},\ ([0-9]{2})\ ([A-Z][a-z]{2})\ ([0-9]{4})\ ([0-9]{2}):([0-9]{2}):([0-9]{2})\ \+0000$ ]]; then
        local day="${BASH_REMATCH[1]}"
        local month_name="${BASH_REMATCH[2]}"
        local year="${BASH_REMATCH[3]}"
        local hour="${BASH_REMATCH[4]}"
        local minute="${BASH_REMATCH[5]}"
        local second="${BASH_REMATCH[6]}"
        
        local month_num="${months[$month_name]}"
        
        if [[ -n "$month_num" ]]; then
            echo "\"${year}-${month_num}-${day}T${hour}:${minute}:${second}Z\""
        else
            echo "$old_date"
        fi
    else
        echo "$old_date"
    fi
}

total_files=0
converted_files=0



# Utiliser find pour obtenir tous les fichiers .md
while IFS= read -r -d '' file; do
    if [[ -f "$file" ]]; then
        # Lire le contenu du fichier
        content=$(cat "$file")
        original_content="$content"
        
        # Chercher les lignes avec l'ancien format de date
        if [[ $content =~ date:\ ([A-Z][a-z]{2},\ [0-9]{2}\ [A-Z][a-z]{2}\ [0-9]{4}\ [0-9]{2}:[0-9]{2}:[0-9]{2}\ \+0000) ]]; then
            ((total_files++))
            
            # Remplacer toutes les occurrences de dates dans ce fichier
            while [[ $content =~ (.*date:\ )([A-Z][a-z]{2},\ [0-9]{2}\ [A-Z][a-z]{2}\ [0-9]{4}\ [0-9]{2}:[0-9]{2}:[0-9]{2}\ \+0000)(.*) ]]; do
                old_date="${BASH_REMATCH[2]}"
                new_date=$(convert_date "$old_date")
                content="${BASH_REMATCH[1]}${new_date}${BASH_REMATCH[3]}"
            done
            
            # Écrire le contenu modifié dans le fichier si il y a eu des changements
            if [[ "$content" != "$original_content" ]]; then
                echo "$content" > "$file"
                ((converted_files++))
                echo "Converti: $file"
            fi
        fi
    fi
done < <(find "../content/jsp" -name "*.md" -print0 2>/dev/null)

echo "Conversion terminée!"
echo "Fichiers traités: $converted_files sur $total_files fichiers avec des dates à convertir"