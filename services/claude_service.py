import logging
import anthropic
from config import Config

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Tu es un expert en business en ligne, marketing digital et entrepreneuriat.
Tu dois generer un plan business complet, actionnable et realiste.
Reponds TOUJOURS en francais. Structure ta reponse EXACTEMENT avec ces sections, en utilisant
ces titres Markdown:

## 1. Idee Business Personnalisee
## 2. Plan d'Action 30 Jours
## 3. Strategie Marketing
## 4. 5 Scripts TikTok
## 5. Plan de Monetisation
## 6. Estimation des Revenus
## 7. Outils Necessaires
## 8. Conseils Mindset

Sois precis, concret et donne des chiffres realistes. Pas de blabla generique.
Chaque section doit contenir du contenu detaille et actionnable."""


def build_user_prompt(profile: dict) -> str:
    return f"""Genere un plan business complet et personnalise pour ce profil:

- Age: {profile['age']} ans
- Budget de depart: {profile['budget']} EUR
- Competences: {profile['skills']}
- Temps disponible par semaine: {profile['available_time']}h
- Pays: {profile['country']}
- Objectif financier mensuel: {profile['financial_goal']} EUR/mois
- Centres d'interet: {profile.get('interests', 'Non precise')}
- Niveau d'experience: {profile.get('experience_level', 'Debutant')}

Genere les 8 sections demandees avec du contenu concret et personnalise.
Pour les scripts TikTok, donne le texte exact a dire avec les timecodes.
Pour le plan 30 jours, donne les actions jour par jour.
Pour l'estimation des revenus, donne mois 1, mois 3, mois 6 et mois 12."""


def generate_business_plan(profile: dict) -> str | None:
    if not Config.ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY is not set")
        return None

    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    try:
        message = client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=Config.CLAUDE_MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_user_prompt(profile)}],
        )
        return message.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {type(e).__name__}: {e}")
        raise
