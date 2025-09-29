import sys

from scripts import CheckLinks

def main():
    tests = [
        ("Vérification des liens", CheckLinks.run),
    ]

    erreurs = 0

    print("Lancement de la suite de tests\n")
    for nom, test in tests:
        print(f"=== {nom} ===")
        ok = test()
        print()
        if not ok:
            erreurs += 1

    print("Résumé :")
    print(f"   {len(tests) - erreurs} tests passés ✅")
    print(f"   {erreurs} tests échoués ❌")

    sys.exit(1 if erreurs > 0 else 0)


if __name__ == "__main__":
    main()
