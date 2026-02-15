# AI Business Generator

Application web SaaS qui genere des plans business personnalises via l'IA Claude.

## Installation locale

### Prerequis
- Python 3.10+
- Cle API Anthropic (https://console.anthropic.com/)

### Etapes

```bash
# 1. Cloner le projet
cd ai-business-generator

# 2. Creer un environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Installer les dependances
pip install -r requirements.txt

# 4. Configurer la cle API
cp .env.example .env
# Editer .env et ajouter votre cle ANTHROPIC_API_KEY

# 5. Lancer
python app.py
```

L'app sera accessible sur `http://localhost:5000`

## Configuration

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Cle API Anthropic (obligatoire) |
| `SECRET_KEY` | Cle secrete Flask pour les sessions |

## Deploiement sur Render

1. Creer un compte sur [render.com](https://render.com)
2. New > Web Service > connecter le repo GitHub
3. Parametres :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
4. Ajouter la variable d'environnement `ANTHROPIC_API_KEY` dans les settings
5. Deployer

## Deploiement sur Railway

1. Creer un compte sur [railway.app](https://railway.app)
2. New Project > Deploy from GitHub repo
3. Ajouter la variable d'environnement `ANTHROPIC_API_KEY`
4. Railway detecte automatiquement le `Procfile`

## Structure

```
ai-business-generator/
├── app.py                  # Application Flask principale
├── config.py               # Configuration
├── Procfile                # Commande de demarrage (deploiement)
├── requirements.txt        # Dependances Python
├── services/
│   └── claude_service.py   # Integration API Claude
├── utils/
│   ├── pdf_generator.py    # Export PDF
│   └── rate_limiter.py     # Limitation d'usage
├── templates/
│   ├── base.html           # Template de base
│   ├── index.html          # Formulaire
│   ├── result.html         # Affichage des resultats
│   └── paywall.html        # Page paywall
└── static/
    ├── css/style.css       # Styles
    └── js/main.js          # JavaScript
```

## Stack

- **Backend** : Flask (Python)
- **IA** : Claude API (Anthropic)
- **PDF** : WeasyPrint + Markdown
- **Frontend** : HTML/CSS vanilla
