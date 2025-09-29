import subprocess
import os
import sys

def get_modified_files():
    try:
        # Récupère les fichiers modifiés ou ajoutés entre la base de la PR et le HEAD
        result = subprocess.run(
            ['git', 'diff', '--name-status', 'origin/main...HEAD'],
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

def check_files_empty(files):
    empty_files = []
    for file_path in files:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_path)
    return empty_files

if __name__ == '__main__':
    modified_files = get_modified_files()
    if not modified_files:
        print("Aucun fichier modifié ou ajouté.")
        sys.exit(0)

    print("Fichiers modifiés ou ajoutés :", modified_files)
    empty_files = check_files_empty(modified_files)

    if empty_files:
        print("Les fichiers suivants sont vides :")
        for f in empty_files:
            print(" -", f)
        sys.exit(1)

    print("Pas de fichier vide")
    sys.exit(0)
