
## Sommaire

1. [Équipe](#équipe)
2. [Gestion de projet et Qualité](#gestion-de-projet-et-qualité)
   - [Versions et Releases](#gestion-de-projet-et-qualité)
   - [Documentation](#gestion-de-projet-et-qualité)
   - [ODJs et Comptes-rendus](#gestion-de-projet-et-qualité)
3. [Contexte général](#contexte-général)
4. [Déploiement site Hugo sur VM](#déploiement-site-hugo-sur-vm)
5. [Scripts](#scripts)
   - [install.sh](#installsh)

## Équipe

L'équipe de ce projet est constitué de 6 personnes. Voici leur noms et leurs rôles:

| Nom du membre de l'équipe                                   | Rôle dans l'équipe                |
|-------------------------------------------------------------|-----------------------------------|
| [Ethan Besse](https://github.com/LeJoker747)                | Développeur                       |
| [Matthias Lionardo](https://github.com/mtthIA)              | Product Owner, Développeur        |
| [Naila BON](https://github.com/naila-bon)                   | Développeuse                      |
| [Adrien FAURÉ](https://github.com/AirbnbEcoPlus)            | SCRUM Master, Développeur         |
| [Matthias Papa-Patsoumoudu](https://github.com/Matthias426) | Développeur                       |
| [Mete YALCIN](https://github.com/MeteIsCoding)              | Développeur                       |

Responsable enseignant de l'équipe : [Jean-Michel Bruel](jean-michel.bruel@irit.fr) & [Yahn Formanczak](yahn.formanczak@univ-tlse2.fr) 

## Gestion de projet et Qualité

Chaque sprint (deux semaines) nous livrons une nouvelle version de notre application (release).
Nous utilisons pour cela les fonctionnalités de GitHub pour les [Releases](https://docs.github.com/en/repositories/releasing-projects-on-github).

- Version courante : [v1.0.0]()
- Lien vers la doc technique : [Documentation technique](https://github.com/gdr-gpl/gdr-gpl/wiki/Documentation-Technique--%E2%80%90-GDR%E2%80%90GPL)
- Lien vers la doc utilisateur : [Documentation utilisateur](https://github.com/gdr-gpl/gdr-gpl/wiki/Documentation-Utilisateur-%E2%80%90-GDR%E2%80%90GPL)

- Liste des ODJs et leurs CRs :

  | Ordres du Jour | Compte-rendus |
  |----------------|---------------|
  | [ODJ 03-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Ordre%20du%20jour%20n%C2%B01%20SAE%20S5.01.pdf) | [CR 03-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Compte%20rendu%20n%C2%B01%20SAE%20S5.01.pdf)|
  | [ODJ 08-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Ordre%20du%20jour%20n%C2%B02%20SAE%20S5.01.pdf) | [CR 08-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Compte%20rendu%20n%C2%B02%20SAE%20S5.01.pdf)|


## Contexte général

Le site existant, construit sur la plateforme WordPress, présente plusieurs inconvénients: il est considéré comme peu pratique, peu convivial et complexe à maintenir. Par ailleurs, son fonctionnement ne favorise pas son utilisation par les membres de la communauté de recherche.

Il a donc été décidé de procéder à une refonte complète du site en s’appuyant sur Hugo mais aussi GitHub pour les vérifications et assurer la fiabilité et la qualité des contenus.

Ce choix permet :

- d’automatiser la génération et la mise à jour des pages web,

- d’améliorer la fiabilité et la rapidité du site

Le but du projet est de créer un site moderne et collaboratif pour le GDR. Les informations (participants, laboratoires, nouvelles, publications) seront structurées en fichiers Markdown, facilitant à Hugo la création automatique des pages HTML.

L'emploi de GitHub Actions garantira un déploiement automatisé, tout en incluant des contrôles (orthographe, validation des données) .

Également le site respectera la charte graphique existante et toutes les contraintes imposées.

#### Site GdR GPL <br>
[Site actuel](https://gdr-gpl.cnrs.fr/) <br>
[Site du CNRS](https://mygdr.hosted.lip6.fr/accueilGDR/7/10)


### Déploiement site Hugo sur VM

## Scripts

### `install.sh`

Installe les dépendances :

- `git`
- `nginx`
- `hugo v0.148.0` (version spécifique)

```
./scripts/install.sh
```

