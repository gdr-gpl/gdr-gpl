<div align="center">
  <table border="0" cellpadding="20" cellspacing="0">
    <tr>
      <td align="center">
        <img src="./static/assets/logo-cnrs.png" alt="CNRS" height="80"  />
      </td>
      <td align="center" style="font-size: 24px; font-weight: bold; color: #2c3e50;">
        GDR SDL<br>
        <span style="font-size: 16px; color: #7f8c8d;">Site Web Moderne et Collaboratif</span>
      </td>
      <td align="center">
        <img src="./static/assets/logo-iut.png" alt="IUT Blagnac" height="80"/>
      </td>
    </tr>
  </table>
  
  <hr style="width: 50%; margin: 20px auto; border: 2px solid #3498db;">
</div>

# GDR SDL - Site Web

![Version](https://img.shields.io/github/v/release/gdr-gpl/gdr-gpl)

Site web moderne et collaboratif pour le GDR SDL (Groupement de Recherche Sciences du Logiciel) - unité CNRS Sciences informatiques de la communauté scientifique française du génie logiciel et de la programmation.

## Sommaire

1. [Équipe](#équipe)
2. [Architecture technique](#architecture-technique)
3. [Gestion de projet et Qualité](#gestion-de-projet-et-qualité)
   - [Versions et Releases](#versions-et-releases)
   - [Documentation](#documentation)
   - [ODJs et Comptes-rendus](#odjs-et-comptes-rendus)
   - [Product Backlog](#product-backlog)
4. [Contexte général](#contexte-général)
5. [Chiffrage du projet](#chiffrage-du-projet)
6. [Tests](#tests)
7. [Scripts](#scripts)
   - [install.sh](#installsh)

## Équipe

L'équipe de ce projet est constitué de 6 personnes. Voici leur noms et leurs rôles:

| Nom du membre de l'équipe                                   | Rôle dans l'équipe                | GitHub |
|-------------------------------------------------------------|-----------------------------------|---------|
| [Ethan Besse](https://github.com/LeJoker747)                | Développeur                       | [@LeJoker747](https://github.com/LeJoker747) |
| [Matthias Lionardo](https://github.com/mtthIA)              | Product Owner, Développeur        | [@mtthIA](https://github.com/mtthIA) |
| [Naila BON](https://github.com/naila-bon)                   | Développeuse                      | [@naila-bon](https://github.com/naila-bon) |
| [Adrien FAURÉ](https://github.com/AirbnbEcoPlus)            | SCRUM Master, Développeur         | [@AirbnbEcoPlus](https://github.com/AirbnbEcoPlus) |
| [Matthias Papa-Patsoumoudu](https://github.com/Matthias426) | Développeur                       | [@Matthias426](https://github.com/Matthias426) |
| [Mete YALCIN](https://github.com/MeteIsCoding)              | Développeur                       | [@MeteIsCoding](https://github.com/MeteIsCoding) |

Responsable enseignant de l'équipe : [Yahn Formanczak](mailto:yahn.formanczak@univ-tlse2.fr)  
Client : [Jean-Michel Bruel](mailto:jean-michel.bruel@irit.fr)
## Architecture technique

### Technologies utilisées
- **Hugo** v0.148.0 - Générateur de sites statiques
- **GitHub Actions** - CI/CD
- **Markdown** - Format de contenu

### Thème personnalisé
Le site utilise un thème personnalisé développé spécifiquement pour ce projet :
- **Repository du thème** : [https://github.com/gdr-gpl/theme](https://github.com/gdr-gpl/theme) (et les commits correspondants)

## Gestion de projet et Qualité

### Versions et Releases
Chaque sprint (deux semaines) nous livrons une nouvelle version de notre application (release).
Nous utilisons pour cela les fonctionnalités de GitHub pour les [Releases](https://docs.github.com/en/repositories/releasing-projects-on-github).

- Version courante : [v1.0.0](https://github.com/gdr-sdl/gdr-sdl/releases/tag/v1.0.0)

### Documentation
- Lien vers la doc technique : [Documentation technique](https://github.com/gdr-sdl/gdr-sdl/wiki/Documentation-Technique--%E2%80%90-GDR%E2%80%90GPL)
- Lien vers la doc utilisateur : [Documentation utilisateur](https://github.com/gdr-sdl/gdr-sdl/wiki/Documentation-Utilisateur-%E2%80%90-GDR%E2%80%90GPL)

### ODJs et Comptes-rendus

Liste des ODJs et leurs CRs :

| Sprint | Période | Ordres du Jour | Compte-rendus | Release | Status |
|--------|---------|----------------|---------------|---------|---------|
| Sprint 0 | 01/09 - 05/09/2025 | [ODJ 03-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Ordre%20du%20jour%20n%C2%B01%20SAE%20S5.01.pdf) | [CR 03-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Compte%20rendu%20n%C2%B01%20SAE%20S5.01.pdf) | [v0.0.0](https://github.com/gdr-gpl/gdr-gpl/releases) | Terminé |
| Sprint 1 | 08/09 - 19/09/2025 | [ODJ 08-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Ordre%20du%20jour%20n%C2%B02%20SAE%20S5.01.pdf) | [CR 08-09-2025](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/R%C3%A9unions/Compte%20rendu%20n%C2%B02%20SAE%20S5.01.pdf) | [v1.0.0](https://github.com/gdr-gpl/gdr-gpl/releases) | Terminé |
| Sprint 2 | 22/09 - 03/10/2025 | Sprint en cours | À venir | À venir | En cours |

### Product Backlog

Voici les principales fonctionnalités développées et prévues :

**Fonctionnalités réalisées :**
- Conversion des données WordPress vers Hugo/Markdown
- Création du thème personnalisé respectant la charte graphique
- Mise en place de l'architecture Hugo
- Configuration du déploiement automatisé

**Fonctionnalités en cours :**
- Optimisation des performances
- Finalisation des pages de contenu
- Tests de déploiement

**Fonctionnalités prévues :**
- Système de contribution pour la communauté
- Automatisation complète des mises à jour
- Validation orthographique automatique

Pour plus de détails sur les tâches spécifiques, consultez nos [Issues GitHub](https://github.com/gdr-gpl/gdr-gpl/issues).

## Contexte général

Le site existant, construit sur la plateforme WordPress, présente plusieurs inconvénients: il est considéré comme peu pratique, peu convivial et complexe à maintenir. Par ailleurs, son fonctionnement ne favorise pas son utilisation par les membres de la communauté de recherche.

Il a donc été décidé de procéder à une refonte complète du site en s'appuyant sur Hugo mais aussi GitHub pour les vérifications et assurer la fiabilité et la qualité des contenus.

Ce choix permet :

- d'automatiser la génération et la mise à jour des pages web,
- d'améliorer la fiabilité et la rapidité du site

Le but du projet est de créer un site moderne et collaboratif pour le GDR. Les informations (participants, laboratoires, nouvelles, publications) seront structurées en fichiers Markdown, facilitant à Hugo la création automatique des pages HTML.

L'emploi de GitHub Actions garantira un déploiement automatisé, tout en incluant des contrôles (orthographe, validation des données).

Également le site respectera la charte graphique existante et toutes les contraintes imposées.

#### Site GdR SDL 
[Site actuel](https://gdr-gpl.cnrs.fr/) 
[Site du CNRS](https://mygdr.hosted.lip6.fr/accueilGDR/7/10)

## Chiffrage du projet

Le chiffrage détaillé du projet est disponible ici :
[Chiffrage du projet (PDF)](https://github.com/gdr-gpl/gdr-gpl/blob/dev/Documents/Chiffrage.pdf)

## Tests

**Note importante** : Sur demande explicite du client (Jean-Michel Bruel), aucun plan de tests formel n'a été mis en place pour ce projet. Le client a indiqué que les tests automatisés n'étaient pas nécessaires dans le contexte de cette refonte de site web statique.

La qualité est néanmoins assurée par :
- Validation manuelle
- Code review sur les PR

## Contact

Pour toute question concernant le projet :
- **Issues GitHub** : [Ouvrir une issue](https://github.com/gdr-gpl/gdr-gpl/issues)
- **Email équipe** : Contacter via les profils GitHub des membres
- **Responsables pédagogiques** : jean-michel.bruel@irit.fr, yahn.formanczak@univ-tlse2.fr

---
