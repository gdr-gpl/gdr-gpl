# Script PowerShell pour convertir les dates du format ancien au nouveau format
# Format ancien: Thu, 05 Dec 2024 17:10:56 +0000
# Format nouveau: "2024-12-05T17:10:56Z"

function Convert-DateFormat {
    param (
        [string]$OldDateString
    )
    
    # Mapping des mois en anglais vers numéros
    $MonthMap = @{
        'Jan' = '01'; 'Feb' = '02'; 'Mar' = '03'; 'Apr' = '04'
        'May' = '05'; 'Jun' = '06'; 'Jul' = '07'; 'Aug' = '08'
        'Sep' = '09'; 'Oct' = '10'; 'Nov' = '11'; 'Dec' = '12'
    }
    
    # Pattern regex pour parser la date
    $Pattern = '([A-Z][a-z]{2}), (\d{2}) ([A-Z][a-z]{2}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) \+0000'
    
    if ($OldDateString -match $Pattern) {
        $Day = $Matches[2]
        $Month = $MonthMap[$Matches[3]]
        $Year = $Matches[4]
        $Hour = $Matches[5]
        $Minute = $Matches[6]
        $Second = $Matches[7]
        
        return "`"$Year-$Month-${Day}T${Hour}:${Minute}:${Second}Z`""
    }
    
    return $OldDateString
}

# Obtenir tous les fichiers .md dans le dossier content et ses sous-dossiers
$Files = Get-ChildItem -Path "c:\Users\Etudiant\Downloads\content" -Filter "*.md" -Recurse

$TotalFiles = 0
$ConvertedFiles = 0

foreach ($File in $Files) {
    $Content = Get-Content -Path $File.FullName -Raw
    $OriginalContent = $Content
    
    # Pattern pour trouver les lignes avec l'ancien format de date
    $DatePattern = 'date: ([A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2} \+0000)'
    
    if ($Content -match $DatePattern) {
        $TotalFiles++
        
        # Remplacer toutes les occurrences de dates dans ce fichier
        $Content = [regex]::Replace($Content, $DatePattern, {
            param($Match)
            $OldDate = $Match.Groups[1].Value
            $NewDate = Convert-DateFormat -OldDateString $OldDate
            return "date: $NewDate"
        })
        
        # Écrire le contenu modifié dans le fichier
        if ($Content -ne $OriginalContent) {
            $Content | Set-Content -Path $File.FullName -NoNewline
            $ConvertedFiles++
            Write-Host "Converti: $($File.FullName)"
        }
    }
}

Write-Host "Conversion terminée!"
Write-Host "Fichiers traités: $ConvertedFiles sur $TotalFiles fichiers avec des dates à convertir"
