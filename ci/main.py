import sys

from scripts import CheckLinks
from scripts import CheckEmptyFiles
from scripts import CheckImages
from scripts import GenerateDocumentation
from scripts import CheckDates

def main():
    tests = [
        ("Vérification des liens", CheckLinks.run),
        ("Vérification des fichiers vides", CheckEmptyFiles.run),
        ("Vérification des fichiers dates", CheckDates.run),
        ("Vérification des et compression des images", CheckImages.run),
        ("Génération de la documentation", GenerateDocumentation.run),
    ]

    erreurs = 0

    print("Lancement de la suite de tests\n")
    for nom, test in tests:
        print(f"=== {nom} ===")
        error = test()
        print()
        if error:
            erreurs += 1

    print("Résumé :")
    print(f"   {len(tests) - erreurs} tests passés ✅")
    print(f"   {erreurs} tests échoués ❌")

    sys.exit(1 if erreurs > 0 else 0)


if __name__ == "__main__":
    main()
