# 📊 Dashboard Emploi — Ingénierie & Industrie en France

> Application Python qui récupère en temps réel les offres d'emploi du marché français (alternance, CDI, CDD, stage, freelance) pour **16 domaines de l'ingénierie**, les visualise dans un dashboard interactif et permet de postuler directement.

---

## 🎯 Objectif du projet

Aider les étudiants et professionnels de l'ingénierie à **trouver rapidement des offres d'emploi ciblées en France**, avec une interface claire, des graphiques de tendances et un accès direct aux candidatures — le tout sans installation complexe.

---

## ✨ Fonctionnalités

- 🔍 **Recherche ciblée** par domaine (Data & IA, Génie Mécanique, Cybersécurité, BTP, Biomédical...)
- 📋 **16 domaines d'ingénierie** couverts avec des mots-clés optimisés
- 🤝 **5 types de contrats** : Alternance, CDI, CDD, Stage, Freelance
- 📊 **Dashboard visuel** avec 4 graphiques interactifs :
  - Répartition par type de contrat
  - Top 10 des villes qui recrutent
  - Top 15 des intitulés de postes
  - Offres par mot-clé de recherche
- 🔎 **Filtre en temps réel** sur le tableau des offres
- 🟢 **Bouton Postuler** qui redirige vers le site de recrutement de l'entreprise
- ⬇️ **Export CSV** compatible Excel (encodage UTF-8, séparateur point-virgule)
- ✅ **Zéro installation** — uniquement des modules natifs Python

---

## 🗂️ Domaines couverts

| Catégorie | Domaines |
|---|---|
| Sciences Appliquées & Technologies | Data & IA, Génie Informatique, Cybersécurité, Cloud & Réseaux |
| Industrie & Production | Génie Mécanique, Électrique, Industriel, Aérospatial, Chimique |
| Bâtiment, TP & Environnement | Génie Civil & BTP, Environnement & Énergies |
| Sciences du Vivant | Génie Biomédical, Agroalimentaire |
| Domaines Supplémentaires | Nucléaire & Énergie, Naval & Maritime |

---

## 🛠️ Technologies utilisées

| Technologie | Usage |
|---|---|
| `Python 3.x` | Langage principal |
| `urllib` | Appels à l'API Adzuna (module natif) |
| `json` | Parsing des réponses API |
| `webbrowser` | Ouverture automatique du dashboard |
| `Chart.js` | Graphiques interactifs dans le dashboard HTML |
| `Adzuna API` | Source des données d'offres d'emploi en temps réel |

---

## 🚀 Installation & Lancement

### Prérequis
- Python 3.8 ou supérieur
- Connexion internet (pour l'appel API)

### Lancement

```bash
python dashboard.py
```

Le programme affiche un menu interactif dans le terminal :

```
══════════════════════════════════════════════════════════════
   DASHBOARD EMPLOI — INGENIERIE & INDUSTRIE EN FRANCE
══════════════════════════════════════════════════════════════

  [Sciences Appliquees & Technologies]
     1. Data & Intelligence Artificielle
     2. Genie Informatique & Developpement
     3. Cybersecurite
     4. Cloud & Reseaux Telecoms
  ...

  Choisis ton domaine (1-16) :
  Type de contrat (A=Alternance / B=CDI / C=CDD / D=Stage / E=Freelance / F=Toutes) :
```

Après sélection, le dashboard s'ouvre automatiquement dans le navigateur.

---

## 📁 Structure du projet

```
dashboard-emploi-ingenierie/
│
├── dashboard.py        # Script principal — menu + API + génération HTML
├── dashboard.html      # Dashboard généré (créé automatiquement à l'exécution)
└── README.md           # Documentation du projet
```

---

## 📸 Aperçu

> *(Ajoute ici une capture d'écran de ton dashboard une fois lancé)*
> 
> Tu peux glisser une image directement dans l'éditeur GitHub après avoir créé le repo.

---

## 🔌 Source des données

Les données proviennent de l'**API officielle Adzuna** — plateforme d'emploi européenne agrégeant des milliers d'offres en temps réel depuis les sites des entreprises françaises.

- API gratuite : [developer.adzuna.com](https://developer.adzuna.com)
- Couverture : France entière
- Mise à jour : à chaque exécution du script

---

## 📈 Ce que ce projet démontre

- Consommation d'une **API REST** externe avec authentification
- **Traitement et nettoyage de données** JSON en Python pur
- **Génération dynamique de contenu HTML** avec visualisations Chart.js
- Conception d'une **interface utilisateur en ligne de commande**
- Export de données au format **CSV compatible Excel**
- Déduplication et tri intelligent des résultats

---

## 👤 Auteur

**Derick Guieto**  
Étudiant en classe préparatoire — Spécialisation Data Science  
📧 tchouataderick@gmail.com  

---

## 📄 Licence

Ce projet est open source — libre d'utilisation et de modification.
