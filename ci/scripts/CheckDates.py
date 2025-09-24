import os
import re
from datetime import datetime
from CheckLinks import FindAllMarkdown

def getDate(dossierPath):
    fichier_md = FindAllMarkdown(dossierPath)
    erreurs = [] 
    erreur_trouvee = False

    for each_file in fichier_md:
        try:
            with open(each_file, 'r', encoding='utf-8') as f:
                date_found = False
                for i in range(10):
                    line = f.readline()
                    if not line:
                        break
                    date_trouvee = re.search(r'^date:\s*"?(.+?)"?$', line.strip())
                    if date_trouvee:
                        date_return = date_trouvee.group(1).strip()
                        try:
                            date_ = datetime.strptime(date_return, "%Y-%m-%dT%H:%M:%SZ")
                            if date_ > datetime.now():
                                erreurs.append(f"[{each_file}]  Date dans le futur : {date_return}")
                                erreur_trouvee = True
                            date_found = True
                            break
                        except ValueError:
                            erreurs.append(f"[{each_file}]  Format invalide : {date_return}")
                            erreur_trouvee = True
                            date_found = True
                            break
                if not date_found:
                    erreurs.append(f"[{each_file}]  Aucune date trouvée")
                    erreur_trouvee = True
        except FileNotFoundError:
            erreurs.append(f"[{each_file}]  Fichier introuvable")
            erreur_trouvee = True

    if erreurs:
        print("-------- Erreurs détectées  --------- ")
        for erreur in erreurs:
            print(erreur)
    else:
        print("Aucune erreur détectée.")

    return 1 if erreur_trouvee else 0

if __name__ == "__main__":
    result = getDate("content/")
    print("Code de retour :", result)
