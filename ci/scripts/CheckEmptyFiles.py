import subprocess
import os
import sys

def get_modified_files():
    try:
        # Récupère les fichiers modifiés ou ajoutés entre la base de la PR et le HEAD
        result = subprocess.run(
            ['git', 'diff', '--name-status', 'origin/dev...HEAD'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        files = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            status, path = line.strip().split('\t', 1)
            if status in ['A', 'M']:  # A: added, M: modified
                files.append(path)
        return files

    except subprocess.CalledProcessError as e:
        print("Erreur lors de l’exécution de git diff:", e.stderr)
        sys.exit(1)

def run() :
    erreurs = False

    #Récupération des fichiers modifiés
    allModifiedFiles = get_modified_files()

#Recherche des fichiers vides
    empty_files = []
    for file_path in allModifiedFiles:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_path)
    #Affichage des fichiers vides s'il y en a
    if len(empty_files) > 0 :  
        erreurs = True
        print("Les fichiers suivants sont vides :")
        for file in empty_files : 
            print(file)
    else :
        print("Aucun fichier modifié n'est vide")
    return erreurs

if __name__ == "__main__":
    run()