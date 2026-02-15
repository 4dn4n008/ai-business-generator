import sys
import os
import logging
import traceback
from flask import Flask, render_template, request, session, redirect, url_for
from config import Config
from services.claude_service import generate_business_plan
from utils.rate_limiter import can_generate, increment_usage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERSION = "2.0"

# Fix paths for PyInstaller
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
else:
    app = Flask(__name__)

app.config.from_object(Config)


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled error: {traceback.format_exc()}")
    return render_template("index.html", error=f"Erreur: {e}"), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not can_generate(session):
        return redirect(url_for("paywall"))

    profile = {
        "age": request.form.get("age"),
        "budget": request.form.get("budget"),
        "skills": request.form.get("skills"),
        "available_time": request.form.get("available_time"),
        "country": request.form.get("country"),
        "financial_goal": request.form.get("financial_goal"),
        "interests": request.form.get("interests", ""),
        "experience_level": request.form.get("experience_level", "debutant"),
    }

    missing = [k for k in ["age", "budget", "skills", "country", "financial_goal"] if not profile[k]]
    if missing:
        return render_template("index.html", error="Veuillez remplir tous les champs obligatoires.")

    try:
        logger.info("Starting generation...")
        result = generate_business_plan(profile)
        if result is None:
            return render_template("index.html", error="Cle API non configuree. Contactez l'administrateur.")
        logger.info(f"Generation OK, length: {len(result)}")
        increment_usage(session)
        return render_template("result.html", result=result, profile=profile)
    except Exception as e:
        logger.error(f"Generation failed: {traceback.format_exc()}")
        return render_template("index.html", error=f"Erreur: {e}")


@app.route("/test-api")
def test_api():
    """Quick API test - returns plain text, no template."""
    import requests as req
    try:
        headers = {
            "x-api-key": Config.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": Config.CLAUDE_MODEL,
            "max_tokens": 100,
            "messages": [{"role": "user", "content": "Dis juste: OK ca marche"}],
        }
        resp = req.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers, timeout=30)
        return f"Status: {resp.status_code}\nResponse: {resp.text[:500]}"
    except Exception as e:
        return f"Error: {e}"


@app.route("/paywall")
def paywall():
    return render_template("paywall.html")


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    api_key = Config.ANTHROPIC_API_KEY
    return {
        "version": VERSION,
        "status": "ok",
        "api_key_set": bool(api_key),
        "api_key_prefix": api_key[:20] + "..." if api_key else "NOT SET",
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000)
