# Awalino AI

## 📌 Description du projet

Awalino AI est un projet collaboratif visant à développer une application intelligente pour l’apprentissage du Tashelhit et de la Darija.  
L’objectif est de proposer une plateforme moderne, accessible et évolutive, basée sur l’intelligence artificielle, afin de faciliter l’apprentissage des langues locales marocaines et de promouvoir l’inclusion numérique.

Ce dépôt sert de base au développement, au versioning et à la collaboration selon un workflow Git/DevOps structuré.

---

## 👥 Membres de l’équipe

- Hicham  
- Oussama  

---

## 📜 Règles de contribution

- Le dépôt utilise un workflow basé sur des branches et des Pull Requests.
- Toute nouvelle fonctionnalité doit être développée dans une branche dédiée :  
  `feature/nom-de-la-fonctionnalite`
- Les corrections de bugs utilisent des branches :  
  `fix/description-du-bug`
- Les commits doivent être :
  - Clairs
  - Courts
  - Avec un message explicite (ex: `feat: add basic lessons module`)
- Aucune modification directe sur la branche `main` n’est autorisée.
- Toute contribution doit passer par une Pull Request et être relue par l’autre membre de l’équipe.

---

## 🌿 Workflow Git

Branches principales :
- `main` : version stable du projet (production)
- `develop` : branche d’intégration des fonctionnalités

Processus de travail :

1. Créer une branche depuis `develop` :
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/ma-fonctionnalite
   ```
