# Obtenir tous les fichiers .md dans le dossier content et ses sous-dossiers
$Files = Get-ChildItem -Path "content\toutesInfos\attachment" -Filter "*.md" -Recurse

# Initialiser le fichier de sortie (le vider s'il existe déjà)
if (Test-Path "attachment_urls.txt") {
    Remove-Item "attachment_urls.txt"
}

Write-Host "Début de l'extraction des URLs d'attachement..."
Write-Host "Nombre de fichiers trouvés: $($Files.Count)"

foreach ($File in $Files) {
    # Lire le contenu du fichier
    $Content = Get-Content -Path $File.FullName -Raw
    
    # Rechercher la ligne qui contient "attachment_url:"
    if ($Content -match "attachment_url:\s*(.+)") {
        $AttachmentUrl = $matches[1].Trim()
        
        # Ajouter l'URL au fichier de sortie
        Add-Content -Path "attachment_urls.txt" -Value $AttachmentUrl
        
        Write-Host "URL extraite de $($File.Name): $AttachmentUrl"
    }
    else {
        Write-Host "Aucune URL d'attachement trouvée dans $($File.Name)"
    }
}