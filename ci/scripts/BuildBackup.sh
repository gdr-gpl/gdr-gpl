#!/bin/bash

# ============================== #
# ==== Création de backup   ==== #
# ============================== #

# Dossier de backup
dossierBackup="backups"

# On crée le dossier de backup si pas déjà existant
mkdir -p "$dossierBackup"

# date qu'on utilise comme identifiant unique pour nom de fichier
DATE=$(date +"%Y%m%d_%H%M%S")
nomBackup="gdr-gpl_backup_${date}.zip"

# On sauvegarde uniquement les fichiers suivis par git
echo " == Backup en cours... =="
git archive --format=zip -o "$dossierBackup/$nomBackup" HEAD

echo "Backup créé : $dossierBackup/$nomBackup"