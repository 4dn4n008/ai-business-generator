import json
import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

API_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """Tu es un expert en business en ligne, marketing digital et entrepreneuriat.
Reponds en francais. Structure ta reponse avec ces sections Markdown:

## 1. Idee Business Personnalisee
## 2. Plan d'Action 30 Jours
## 3. Strategie Marketing
## 4. 5 Scripts TikTok
## 5. Plan de Monetisation
## 6. Estimation des Revenus
## 7. Outils Necessaires
## 8. Conseils Mindset

Sois precis et concret."""


def build_user_prompt(profile: dict) -> str:
    return f"""Plan business pour: {profile['age']} ans, {profile['budget']} EUR budget, competences: {profile['skills']}, {profile['available_time']}h/sem, {profile['country']}, objectif {profile['financial_goal']} EUR/mois, interets: {profile.get('interests', 'aucun')}, niveau: {profile.get('experience_level', 'debutant')}. Genere les 8 sections."""


def generate_business_plan_stream(profile: dict):
    """Generator that yields text chunks as they arrive from Claude."""
    if not Config.ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY not set")
        yield "Erreur: Cle API non configuree."
        return

    headers = {
        "x-api-key": Config.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    payload = {
        "model": Config.CLAUDE_MODEL,
        "max_tokens": Config.CLAUDE_MAX_TOKENS,
        "stream": True,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": build_user_prompt(profile)}],
    }

    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=120, stream=True)
        resp.raise_for_status()

        for line in resp.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            data_str = decoded[6:]
            if data_str.strip() == "[DONE]":
                break
            try:
                event = json.loads(data_str)
                if event.get("type") == "content_block_delta":
                    text = event.get("delta", {}).get("text", "")
                    if text:
                        yield text
            except json.JSONDecodeError:
                continue

    except Exception as e:
        logger.error(f"Claude API error: {e}")
        yield f"\n\nErreur: {e}"
