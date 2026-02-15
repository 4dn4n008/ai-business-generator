import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

API_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """Tu es un expert en business en ligne, marketing digital et entrepreneuriat.
Tu dois generer un plan business complet, actionnable et realiste.
Reponds TOUJOURS en francais. Structure ta reponse avec ces sections Markdown:

## 1. Idee Business Personnalisee
## 2. Plan d'Action 30 Jours
## 3. Strategie Marketing
## 4. 5 Scripts TikTok
## 5. Plan de Monetisation
## 6. Estimation des Revenus
## 7. Outils Necessaires
## 8. Conseils Mindset

Sois precis, concret et donne des chiffres realistes."""


def build_user_prompt(profile: dict) -> str:
    return f"""Genere un plan business personnalise pour ce profil:
- Age: {profile['age']} ans
- Budget: {profile['budget']} EUR
- Competences: {profile['skills']}
- Temps/semaine: {profile['available_time']}h
- Pays: {profile['country']}
- Objectif: {profile['financial_goal']} EUR/mois
- Interets: {profile.get('interests', 'Non precise')}
- Niveau: {profile.get('experience_level', 'Debutant')}

Donne du contenu concret et actionnable pour chaque section."""


def generate_business_plan(profile: dict) -> str | None:
    if not Config.ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY not set")
        return None

    headers = {
        "x-api-key": Config.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    payload = {
        "model": Config.CLAUDE_MODEL,
        "max_tokens": Config.CLAUDE_MAX_TOKENS,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": build_user_prompt(profile)}],
    }

    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        raise
