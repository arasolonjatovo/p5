# P5 — API de prédiction des émissions de gaz à effet de serre (GES) des bâtiments non-reservés à l'habitation

API REST bâtie avec **FastAPI** qui prédit les émissions totales de gaz à effet de serre
(`TotalGHGEmissions`) d'un bâtiment à partir de ses caractéristiques, à l'aide d'un modèle de
Machine Learning **Gradient Boosting** (scikit-learn) entraîné sur les données de consommation
énergétique des bâtiments de la ville de **Seattle (2016)**.

Chaque prédiction est historisée dans une base **PostgreSQL** (bâtiment, requête d'inférence et
prédiction associée).

---

## Sommaire

- [À propos du projet](#à-propos-du-projet)
  - [Construit avec](#construit-avec)
  - [Architecture](#architecture)
- [Pour commencer](#pour-commencer)
  - [Pré-requis](#pré-requis)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Base de données](#base-de-données)
  - [Lancer l'API](#lancer-lapi)
- [API](#api)
  - [Endpoints](#endpoints)
  - [Exemple de requête](#exemple-de-requête)
- [Tests](#tests)
- [Intégration continue (CI)](#intégration-continue-ci)
- [Structure du projet](#structure-du-projet)
- [Contributeur](#contributeur)

---

## À propos du projet

Ce projet expose un modèle de régression pré-entraîné (`model/gb_pipeline_seattle.pkl`) via une API
HTTP. À partir de quelques caractéristiques d'un bâtiment (type, année de construction, nombre de
bâtiments et d'étages, surface totale), l'API :

1. calcule l'âge du bâtiment (`BuildingAge = année courante − YearBuilt`) ;
2. prédit ses émissions totales de GES avec le pipeline scikit-learn ;
3. enregistre le bâtiment, la requête d'inférence et la prédiction en base PostgreSQL ;
4. retourne la prédiction ainsi que les identifiants créés.

Le jeu de données d'entraînement nettoyé est fourni dans
`data/cleaned_buildings_2016_seattle.csv` et contient les colonnes :
`PrimaryPropertyType`, `YearBuilt`, `NumberofBuildings`, `NumberofFloors`, `PropertyGFATotal`,
`TotalGHGEmissions` (cible).

### Construit avec

- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — framework web / API
- [Uvicorn](https://www.uvicorn.org/) — serveur ASGI
- [Pydantic](https://docs.pydantic.dev/) — validation des données
- [scikit-learn](https://scikit-learn.org/) + [joblib](https://joblib.readthedocs.io/) — modèle ML
- [pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — manipulation des données
- [SQLAlchemy](https://www.sqlalchemy.org/) + [psycopg2](https://www.psycopg.org/) — accès PostgreSQL
- [uv](https://docs.astral.sh/uv/) — gestion de l'environnement et des dépendances
- [pytest](https://docs.pytest.org/) / [pytest-cov](https://pytest-cov.readthedocs.io/) — tests
- [GitHub Actions](https://docs.github.com/actions) — CI

### Architecture

```
Client HTTP
    │  POST /predict
    ▼
FastAPI (src/p5/main.py)
    │
    ├─► Validation Pydantic (src/p5/schemas.py)
    ├─► Modèle ML joblib (model/gb_pipeline_seattle.pkl)
    └─► Persistance SQLAlchemy (src/p5/database.py)
            │
            ▼
        PostgreSQL
        ├── buildings
        ├── ml_requests
        └── ml_predictions
```

---

## Pour commencer

### Pré-requis

- **Python 3.11** ou supérieur
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** (gestionnaire de paquets)
- Un serveur **PostgreSQL** accessible (local ou distant)

Installation de `uv` (si nécessaire) :

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# ou via pip
pip install uv
```

### Installation

Cloner le dépôt puis installer les dépendances dans un environnement virtuel géré par `uv` :

```bash
git clone <url-du-repo>
cd p5

# Crée le .venv et installe toutes les dépendances (y compris dev)
uv sync --all-extras --dev
```

### Configuration

Les paramètres de connexion à la base sont lus depuis des variables d'environnement
(via `python-dotenv`). Copiez le fichier d'exemple puis renseignez vos valeurs :

```bash
cp .env.dist .env
```

Éditez `.env` :

```dotenv
DB_USER=mon_utilisateur
DB_PASSWORD=mon_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
DB_NAME=p5
```

> Le fichier `.env` est ignoré par git (voir `.gitignore`). Ne committez jamais vos identifiants.

### Base de données

L'API insère les données dans trois tables : `buildings`, `ml_requests` et `ml_predictions`.
Créez-les avant de lancer l'API :

```sql
CREATE TABLE buildings (
    id                  SERIAL PRIMARY KEY,
    "PrimaryPropertyType" TEXT        NOT NULL,
    "YearBuilt"           INTEGER     NOT NULL,
    "NumberofBuildings"   REAL        NOT NULL,
    "NumberofFloors"      INTEGER     NOT NULL,
    "PropertyGFATotal"    REAL        NOT NULL,
    "TotalGHGEmissions"   REAL        NOT NULL
);

CREATE TABLE ml_requests (
    id          SERIAL PRIMARY KEY,
    building_id INTEGER REFERENCES buildings(id),
    input_data  JSONB       NOT NULL,
    created_at  TIMESTAMP   DEFAULT now()
);

CREATE TABLE ml_predictions (
    id         SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES ml_requests(id),
    prediction REAL        NOT NULL,
    created_at TIMESTAMP   DEFAULT now()
);
```

### Lancer l'API

```bash
# Mode développement (rechargement automatique)
uv run uvicorn p5.main:app --reload

# ou via la CLI FastAPI
uv run fastapi dev src/p5/main.py
```

L'API est disponible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

Documentation interactive :

- Swagger UI : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API

### Endpoints

| Méthode | Chemin      | Description                                            |
| ------- | ----------- | ------------------------------------------------------ |
| `GET`   | `/`         | Message de statut de l'API                             |
| `GET`   | `/health`   | Vérification de santé (health check)                   |
| `POST`  | `/predict`  | Prédit les émissions de GES et historise la requête    |

**Corps de la requête `/predict`** (`PredictionRequest`) :

| Champ                 | Type    | Contrainte           | Exemple  |
| --------------------- | ------- | -------------------- | -------- |
| `PrimaryPropertyType` | string  | —                    | `Hotel`  |
| `YearBuilt`           | integer | `1800 ≤ x ≤ 2026`    | `1996`   |
| `NumberofBuildings`   | float   | `> 0`                | `1.0`    |
| `NumberofFloors`      | integer | `> 0`                | `11`     |
| `PropertyGFATotal`    | float   | `> 0`                | `103566` |

**Réponse `/predict`** :

```json
{
  "building_id": 1,
  "request_id": 1,
  "prediction": 295.86,
  "building_age": 30
}
```

### Exemple de requête

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PrimaryPropertyType": "Hotel",
    "YearBuilt": 1996,
    "NumberofBuildings": 1.0,
    "NumberofFloors": 11,
    "PropertyGFATotal": 103566
  }'
```

---

## Tests

Les tests utilisent `pytest`. La configuration (`pyproject.toml`) ajoute `src` au `pythonpath`
et cible le dossier `tests`.

```bash
# Exécuter la suite de tests
uv run pytest

# Avec couverture de code
uv run pytest --cov=. tests/
```

---

## Intégration continue (CI)

Le workflow [`.github/workflows/ci_cd.yml`](.github/workflows/ci_cd.yml) s'exécute sur les
`push` et `pull_request` vers les branches `main` et `develop`. Il :

1. installe `uv` et Python 3.11 ;
2. synchronise les dépendances (`uv sync --all-extras --dev`) ;
3. lance la suite de tests (`uv run pytest`) puis la couverture (`uv run pytest --cov`).

---

## Structure du projet

```
p5/
├── data/
│   └── cleaned_buildings_2016_seattle.csv   # Données d'entraînement nettoyées
├── model/
│   └── gb_pipeline_seattle.pkl              # Pipeline Gradient Boosting sérialisé
├── src/
│   └── p5/
│       ├── __init__.py                      # Point d'entrée CLI (main)
│       ├── main.py                          # Application FastAPI + endpoints
│       ├── schemas.py                       # Schémas Pydantic (validation)
│       ├── settings.py                      # Chargement des variables d'environnement
│       └── database.py                      # Connexion SQLAlchemy / PostgreSQL
├── tests/
│   └── test_basic.py                        # Tests
├── .github/workflows/ci_cd.yml              # Pipeline CI
├── .env.dist                                # Modèle de configuration
├── pyproject.toml                           # Métadonnées & dépendances
└── README.md
```

---

## Contributeur

- **Audrey RASOLONJATOVO** — [rasolonjatovo.audrey@gmail.com](mailto:rasolonjatovo.audrey@gmail.com)
