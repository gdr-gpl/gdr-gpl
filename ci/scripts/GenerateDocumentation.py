import os
import re
from pathlib import Path

# Title : Fichier permettant de générer la documentation des scripts, archetypes et structure de content/ du projet

# ======================================================= #
# ==== Génération de la documentation des archetypes ==== #
# ======================================================= #
def GenerateArchetypesDoc(archetypesDir, docsDir):
    """
    Génère la documentation des archetypes Hugo dans un fichier Markdown

    Args :
        archetypesDir : chemin du dossier archetypes/
        docsDir : chemin du dossier docs/ où écrire la doc
    
    Résultat :
        Crée ou écrase docs/archetypes.md avec la documentation générée
    """
    
    # On vérifie si le dossier archetypes existe
    if not os.path.isdir(archetypesDir):
        print(f"Le dossier {archetypesDir} n'existe pas.")
        return

    # On définit le path du fichier de documentation
    os.makedirs(docsDir, exist_ok=True)
    fichierDoc = os.path.join(docsDir, "archetypes.md")
    
    # On commence à écrire le contenu de notre doc
    contenu = "# Archétypes Hugo\n\n"
    contenu += "*Documentation générée automatiquement*\n\n"
    contenu += "Les archétypes sont les modèles les contenus.\n\n"

    # On parcourt tous les fichiers .md dans archetypes/
    for nomFichier in os.listdir(archetypesDir):

        # Si le fichier est un .md alors on récupère le contenu
        if nomFichier.endswith(".md"):
            cheminComplet = os.path.join(archetypesDir, nomFichier)
            nomSansExtension = os.path.splitext(nomFichier)[0]
            
            contenu += f"## {nomSansExtension}\n\n"
            contenu += f"**Fichier :** `{os.path.relpath(cheminComplet)}`\n\n"

            # On lit le contenu du fichier
            try:
                with open(cheminComplet, "r", encoding="utf-8") as fichier:
                    contenuArchetype = fichier.read()

                contenu += "```toml\n"
                contenu += contenuArchetype
                contenu += "\n```\n\n"

                # On recherche des champs
                # Type : (clé = ...)
                champsDetectes = re.findall(r'(\w+)\s*=', contenuArchetype)

                if champsDetectes:
                    contenu += "**Champs définis :**\n"
                    for champ in champsDetectes:
                        contenu += f"- `{champ}`\n"
                    contenu += "\n"

            except Exception as error:
                contenu += f"*Erreur dans la génération de la documenation des archetypes : {error}*\n\n"

    # Write du fichier de documentation
    with open(fichierDoc, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"Documentation des archétypes générée dans {fichierDoc}")


# ==================================================== #
# ==== Génération de la documentation des scripts ==== #
# ==================================================== #
def GenerateScriptsDoc(scriptsDir, docsDir):
    """
    Génère la documentation des scripts Python du projet dans un fichier Markdown

    Args :
        scriptsDir : chemin du dossier contenant les scripts (ex: 'ci/scripts/')
        docsDir : chemin du dossier docs/ où écrire la doc

    Résultat :
        Crée ou écrase docs/scripts.md avec la documentation générée
    """
    
    # On vérifie si le dossier scripts existe
    if not os.path.isdir(scriptsDir):
        return

    # On définit le path du fichier de documentation
    os.makedirs(docsDir, exist_ok=True)
    fichierDoc = os.path.join(docsDir, "scripts.md")

    # On commence à écrire le contenu de notre doc
    contenu = "# Scripts du Projet\n\n"
    contenu += "*Documentation générée automatiquement*\n\n"
    contenu += "Liste des scripts Python présents dans le projet et leur description.\n\n"

    # On parcourt tous les fichiers .py dans scriptsDir
    for nomFichier in os.listdir(scriptsDir):

        # Si le fichier est un .py alors on récupère le contenu
        if nomFichier.endswith(".py") or nomFichier.endswith(".sh"):

            cheminComplet = os.path.join(scriptsDir, nomFichier)
            contenu += f"## {nomFichier}\n\n"
            contenu += f"**Fichier :** `{os.path.relpath(cheminComplet)}`\n\n"

            try:

                # On lit le contenu du script
                with open(cheminComplet, "r", encoding="utf-8") as fichier:
                    contenuScript = fichier.read()

                # On extrait le title depuis le commentaire (qui sera la description car le title dans la doc est le nom du fichier)
                description = ""
                lignes = contenuScript.split('\n')

                # On cherche dans les 10 premières lignes pour être sûr
                for ligne in lignes[:10]:
                    lignePropre = ligne.strip()

                    # On cherche le commentaire "# Title :"
                    # Je sais pas porquoi je l'ai pas nommé "# Description :" dès le début en vrai c'est plus une description qu'un title
                    # Je peux le changer ça me coûte rien
                    if lignePropre.startswith("# Title :"):
                        description = lignePropre.replace("# Title :", "").strip()
                        break

                # Du coup la fameuse ligne de description
                if description:
                    contenu += f"**Description :** {description}\n\n"

                # On extrait les imports principaux
                importsStandard = re.findall(r'^import\s+(\w+)', contenuScript, re.MULTILINE)
                importsFrom = re.findall(r'^from\s+(\w+)', contenuScript, re.MULTILINE)
                
                tousLesImports = importsStandard + importsFrom
                
                if tousLesImports:
                    importsUniques = sorted(set(tousLesImports))
                    contenu += "**Dépendances :** " + ", ".join(importsUniques) + "\n\n"

            except Exception as erreur:
                contenu += f"*Erreur lors de read du fichier {erreur}*\n\n"

    # On write le fichier de documentation
    with open(fichierDoc, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"Documentation des scripts générée dans {fichierDoc}")


# ==================================================== #
# ==== Génération de la documentation de contents ==== #
# ==================================================== #
def GenerateContentDoc(contentDir, docsDir):
    """
    Génère la documentation de la structure de contents/ dans un fichier Markdown

    Args :
        contentDir : chemin du dossier content/
        docsDir : chemin du dossier docs/ où écrire la doc

    Résultat :
        Crée ou écrase docs/content.md avec la documentation générée
    """
    
    # On vérifie si le dossier content existe
    if not os.path.isdir(contentDir):
        return

    # On définit le path du fichier de documentation
    os.makedirs(docsDir, exist_ok=True)
    fichierDoc = os.path.join(docsDir, "content.md")

    # On commence à écrire le contenu de notre doc
    contenu = "# Structure du Contenu\n\n"
    contenu += "*Documentation générée automatiquement*\n\n"
    contenu += "Organisation des contenus du site GDR-GPL.\n\n"

    # On parcourt le dossier content/
    for racine, listeDossiers, listeFichiers in os.walk(contentDir):
        
        # On calcule le niveau de tab basé sur la profondeur dans content/
        profondeur = racine.replace(contentDir, "").count(os.sep)
        
        # On génère les headers selon le niveau
        # On commence à ## pour content/
        niveauTitre = "#" * (profondeur + 2)
        
        # On affiche le nom du dossier
        nomDossier = os.path.basename(racine) or "content"
        contenu += f"{niveauTitre} {nomDossier}/\n\n"
        
        # On compte les fichiers .md dans ce dossier
        fichiersMarkdown = [fichier for fichier in listeFichiers if fichier.endswith('.md')]
        
        if fichiersMarkdown:
            contenu += f"**Fichiers Markdown ({len(fichiersMarkdown)}) :**\n\n"
            
            # On affiche les fichiers
            for fichierMd in fichiersMarkdown:
                cheminComplet = os.path.join(racine, fichierMd)
                contenu += f"- `{fichierMd}`\n"
                
                try:

                    # On lit le contenu du fichier
                    with open(cheminComplet, "r", encoding="utf-8") as fichier:
                        contenuFichier = fichier.read()
                    
                    # On extrait le front matter YAML
                    if contenuFichier.startswith('---'):
                        finFrontMatter = contenuFichier.find('---', 3)
                        
                        if finFrontMatter != -1:
                            metadonnees = contenuFichier[3:finFrontMatter].strip()
                            
                            # On cherche le titre
                            rechercheTitre = re.search(r'^title\s*:\s*["\']?([^"\'\n]+)["\']?', metadonnees, re.MULTILINE)
                            if rechercheTitre:
                                contenu += f"  - Titre: {rechercheTitre.group(1)}\n"
                            
                            # On cherche le type
                            rechercheType = re.search(r'^type\s*:\s*([^\n]+)', metadonnees, re.MULTILINE)
                            if rechercheType:
                                contenu += f"  - Type: {rechercheType.group(1)}\n"
                            
                            # On cherche la date
                            rechercheDate = re.search(r'^date\s*:\s*([^\n]+)', metadonnees, re.MULTILINE)
                            if rechercheDate:
                                contenu += f"  - Date: {rechercheDate.group(1)}\n"
                        
                except Exception as erreur:
                    contenu += f"  - *Erreur lors de la lecture du fichier {cheminComplet} : {erreur}*\n"
                
                contenu += "\n"
            
            # Ajouter si prend beaucoup de temps et espace en prod mais je pense pas
            # # Si il y a plus de 4 fichiers
            # if len(fichiersMarkdown) > 4:
            #     contenu += f"... et {len(fichiersMarkdown) - 4} autres fichiers\n\n"
        
        # On affiche les sous-dossiers
        if listeDossiers:
            contenu += f"**Sous-dossiers ({len(listeDossiers)}) :** {', '.join(listeDossiers)}\n\n"

    # On write le fichier de documentation
    with open(fichierDoc, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"Documentation du contenu du dossier content générée dans {fichierDoc}")


def Run():

    dossierArchetypes = os.path.join("archetypes")
    dossierScripts = os.path.join("ci", "scripts") 
    dossierContent = os.path.join("content")
    dossierDocs = os.path.join("docs")

    GenerateArchetypesDoc(dossierArchetypes, dossierDocs)
    GenerateScriptsDoc(dossierScripts, dossierDocs)
    GenerateContentDoc(dossierContent, dossierDocs)

if __name__ == "__main__":

    Run()
