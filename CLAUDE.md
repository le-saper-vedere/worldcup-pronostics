# CLAUDE.md - Projet Pronostics Coupe du Monde

> Ce fichier donne le contexte à Claude Code pour accompagner le développement.

## 🎯 Vision du Projet

Application web de pronostics pour la Coupe du Monde de football.
- **Sans argent réel** : juste pour le fun entre amis
- **Cible** : groupe de 5-20 amis
- **Stack** : Vue.js (frontend) + Python FastAPI (backend)
- **Budget** : 0€ (hébergement gratuit)

---

## 👤 Profil du Développeur

- **Niveau backend** : Débutant (première API)
- **Connaissances SQL** : Basique (SELECT, INSERT, UPDATE, DELETE)
- **Objectif principal** : Apprendre le développement backend
- **Approche souhaitée** : Mode Coach + Pair Programming

### Comment m'accompagner

```
1. EXPLIQUE le concept avant de coder
2. MONTRE un exemple simple
3. POSE une question pour vérifier ma compréhension
4. GUIDE-MOI pour que je code moi-même
5. CORRIGE et explique si je fais une erreur
```

- Ne donne PAS la solution complète directement
- Pose des questions pour me faire réfléchir
- Explique le "pourquoi", pas juste le "comment"
- Utilise des analogies simples (restaurant, etc.)

---

## 📋 MVP - Fonctionnalités

### Inclus dans le MVP

1. **Auth Slack** : connexion via Slack OAuth
2. **Liste des matchs** : voir tous les matchs (date, équipes, phase, statut)
3. **Pronostiquer** :
   - Score exact (ex: 2-1)
   - Vainqueur simple (1/N/2)
   - Les deux types possibles sur le même match
   - Deadline : 1 heure avant le coup d'envoi
4. **Classement** : leaderboard avec points de chacun
5. **Historique** : voir ses anciens pronostics
6. **Révélation des pronos** :
   - Avant deadline : on voit uniquement SON prono
   - Après deadline : on voit les pronos de TOUS

### Hors MVP (v2)

- Leagues privées multiples
- Monnaie virtuelle
- Badges/achievements
- Notifications push
- Bot Slack
- Scores en temps réel

---

## 🏗️ Architecture

### Structure Monorepo

```
worldcup-pronostics/
├── CLAUDE.md              # Ce fichier
├── README.md
├── .gitignore
│
├── frontend/              # Vue.js (plus tard)
│   └── ...
│
└── backend/               # Python FastAPI
    ├── app/
    │   ├── __init__.py
    │   ├── main.py        # Point d'entrée FastAPI
    │   ├── config.py      # Variables d'environnement
    │   ├── database.py    # Connexion PostgreSQL
    │   │
    │   ├── models/        # SQLAlchemy (tables)
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── team.py
    │   │   ├── match.py
    │   │   └── bet.py
    │   │
    │   ├── schemas/       # Pydantic (validation)
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── match.py
    │   │   └── bet.py
    │   │
    │   ├── routers/       # Endpoints API
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── matches.py
    │   │   ├── bets.py
    │   │   └── leaderboard.py
    │   │
    │   └── services/      # Logique métier
    │       ├── __init__.py
    │       ├── auth_service.py
    │       ├── match_service.py
    │       ├── bet_service.py
    │       └── points_service.py
    │
    ├── alembic/           # Migrations DB
    ├── requirements.txt
    ├── .env.example
    └── .env               # NE PAS COMMIT
```

### Stack Technique

| Composant | Technologie | Hébergement |
|-----------|-------------|-------------|
| Frontend | Vue 3 + Vite + Pinia + TailwindCSS | Vercel |
| Backend | Python 3.11 + FastAPI + SQLAlchemy | Render |
| Database | PostgreSQL | Supabase |
| Auth | Slack OAuth 2.0 | - |

---

## 📊 Modèle de Données

### Table: teams
```sql
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(3) UNIQUE NOT NULL,  -- "FRA", "ARG"
    flag_url VARCHAR(255),
    "group" VARCHAR(1)                -- "A" à "H"
);
```

### Table: matches
```sql
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    team_home_id INTEGER REFERENCES teams(id),
    team_away_id INTEGER REFERENCES teams(id),
    date TIMESTAMP NOT NULL,
    stage VARCHAR(20) NOT NULL,       -- "group", "round16", "quarter", "semi", "final"
    score_home INTEGER,               -- NULL si pas joué
    score_away INTEGER,
    status VARCHAR(20) DEFAULT 'upcoming'  -- "upcoming", "live", "finished"
);
```

### Table: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    slack_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(255),
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table: bets
```sql
CREATE TABLE bets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    match_id INTEGER REFERENCES matches(id),
    type VARCHAR(10) NOT NULL,        -- "exact" ou "winner"
    predicted_home INTEGER,           -- si type = "exact"
    predicted_away INTEGER,
    predicted_winner VARCHAR(1),      -- "1", "N", "2" si type = "winner"
    points_earned INTEGER,            -- calculé après le match
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    UNIQUE(user_id, match_id, type)   -- 1 prono par type par match par user
);
```

---

## 🔌 Endpoints API

### Auth
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/auth/slack` | Redirige vers Slack OAuth |
| GET | `/auth/slack/callback` | Callback après auth |
| GET | `/auth/me` | User connecté |
| POST | `/auth/logout` | Déconnexion |

### Matches
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/matches` | Liste tous les matchs |
| GET | `/matches/{id}` | Détail d'un match |
| GET | `/matches/{id}/bets` | Pronos du match (si deadline passée) |

### Bets
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/bets` | Créer un pronostic |
| PUT | `/bets/{id}` | Modifier un pronostic |
| GET | `/bets/me` | Mes pronostics |

### Leaderboard
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/leaderboard` | Classement général |

### Admin
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/admin/matches` | Créer un match |
| PUT | `/admin/matches/{id}` | Modifier un match |
| PUT | `/admin/matches/{id}/score` | Saisir le score final |

---

## 📏 Règles Métier

### Deadline pronostic
```python
from datetime import datetime, timedelta

def is_bet_allowed(match_date: datetime) -> bool:
    deadline = match_date - timedelta(hours=1)
    return datetime.now() < deadline
```

### Calcul des points (à définir)
```python
# Option suggérée :
# - Score exact : 5 points
# - Bon vainqueur + bonne différence : 3 points
# - Bon vainqueur seul : 1 point
# - Mauvais prono : 0 point
```

### Révélation des pronos
```python
def can_see_others_bets(match_date: datetime) -> bool:
    deadline = match_date - timedelta(hours=1)
    return datetime.now() > deadline
```

---

## 🎓 Parcours d'Apprentissage

Le développeur suit ce parcours progressif :

### Phase 1 : Fondamentaux ✅
- [x] Concept client/serveur
- [x] Verbes HTTP (GET, POST, PUT, DELETE)
- [x] Endpoints et URLs REST
- [x] Codes de réponse HTTP
- [x] Format JSON
- [x] Introduction à FastAPI

### Phase 2 : Premier CRUD (en cours)
- [ ] Setup projet Python + venv
- [ ] Premier endpoint Hello World
- [ ] CRUD en mémoire (sans DB)
- [ ] Paramètres URL et body JSON

### Phase 3 : Base de données
- [ ] SQLAlchemy (ORM)
- [ ] Connexion Supabase
- [ ] Migrations Alembic
- [ ] CRUD avec PostgreSQL

### Phase 4 : Authentification
- [ ] OAuth 2.0 (concept)
- [ ] Slack OAuth
- [ ] JWT tokens
- [ ] Routes protégées

### Phase 5 : Logique Métier
- [ ] Système de paris
- [ ] Vérification deadline
- [ ] Calcul des points
- [ ] Leaderboard

### Phase 6 : Déploiement
- [ ] Render (backend)
- [ ] Variables d'environnement
- [ ] Tests en production

---

## 🚫 Ce que Claude ne doit PAS faire

- Donner la solution complète sans explication
- Coder à la place du développeur sans lui faire comprendre
- Utiliser des concepts avancés non expliqués
- Ignorer les erreurs sans les expliquer
- Aller trop vite sans vérifier la compréhension

---

## ✅ Ce que Claude DOIT faire

- Expliquer chaque nouveau concept avec des analogies
- Poser des questions de vérification
- Encourager le développeur à coder lui-même
- Corriger les erreurs de manière pédagogique
- Célébrer les réussites ! 🎉
- Adapter le rythme au niveau du développeur