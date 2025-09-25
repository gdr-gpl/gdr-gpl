import os
import re
from pathlib import Path

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
        return

    # On définit le path du fichier du fichier de la documentation
    docPath = os.path.join(docsDir, "archetypes.md")

    # Contenu de contexte du fichier
    contenu = "# Archétypes Hugo\n\n"
    contenu += "*Documentation générée automatiquement*\n\n"
    contenu += "Les archétypes sont les modèles les contenus.\n\n"

    #### On parcourt tous les fichiers .md dans archetypes/ ####
    for fichier in os.listdir(archetypesDir):

        # Si le fichier est un .md alors on recupère le contenu
        if fichier.endswith(".md"):
            cheminFichier = os.path.join(archetypesDir, fichier)
            nom = os.path.splitext(fichier)[0]
            contenu += f"## {nom}\n\n"
            contenu += f"**Fichier :** `{os.path.relpath(cheminFichier)}`\n\n"

            # On lit le contenu du fichier
            try:
                with open(cheminFichier, "r", encoding="utf-8") as f:
                    data = f.read()

                contenu += "```toml\n"
                contenu += data
                contenu += "\n```\n\n"

                # On recherche des champs
                # Type = (clé = ...)
                champs = re.findall(r'(\w+)\s*=', data)

                if champs:
                    contenu += "**Champs définis :**\n"
                    for champ in champs:
                        contenu += f"- `{champ}`\n"
                    contenu += "\n"

            except Exception as e:
                contenu += f"*Erreur dans la génération des archetypes : {e}*\n\n"

    # Écriture du fichier de documentation
    with open(docPath, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"Généré : {docPath}")


if __name__ == "__main__":

    # Dossiers archetypes/ et docs/
    archetypesDir = os.path.join("archetypes")
    docsDir = os.path.join("docs")

    GenerateArchetypesDoc(archetypesDir, docsDir)