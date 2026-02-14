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

## 🔁 Schéma du Workflow Git

            feature/ma-fonctionnalite
                     |
                     v
                   develop
                     |
                     v
                    main

Flux de travail :

1. Créer une branche depuis `develop` :
   feature/ma-fonctionnalite

2. Développer et faire des commits sur la branche feature

3. Ouvrir une Pull Request :
   feature/*  →  develop

4. Après validation et tests :
   develop  →  main (Release)

Règles :
- `main` : branche stable (production)
- `develop` : branche d’intégration
- `feature/*` : nouvelles fonctionnalités
- Aucun push direct sur `main` (ni sur `develop` si protégé)
- Tout passe par Pull Request + review