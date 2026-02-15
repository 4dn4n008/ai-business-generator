import sys
import os
import logging
from flask import Flask, render_template, request, session, redirect, url_for, Response, stream_with_context
from config import Config
from services.claude_service import generate_business_plan_stream
from utils.rate_limiter import can_generate, increment_usage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERSION = "3.0"

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
else:
    app = Flask(__name__)

app.config.from_object(Config)


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

    increment_usage(session)

    def stream_page():
        # Send the HTML header
        yield """<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Business Generator - Resultat</title>
<link rel="stylesheet" href="/static/css/style.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head><body>
<nav class="navbar"><a href="/" class="nav-logo"><span class="logo-icon">&#9889;</span> AI Business Generator</a></nav>
<main class="container">
<section class="result-header"><h1>Ton Plan Business est Pret</h1>
<div class="result-actions" style="margin-top:16px">
<button onclick="window.print()" class="btn btn-primary">Telecharger en PDF</button>
<a href="/" class="btn btn-outline">Nouvelle generation</a></div></section>
<div class="profile-summary"><h3>Ton Profil</h3><div class="profile-tags">
<span class="tag">""" + str(profile['age']) + """ ans</span>
<span class="tag">""" + str(profile['budget']) + """ EUR</span>
<span class="tag">""" + str(profile['available_time']) + """h/sem</span>
<span class="tag">""" + str(profile['country']) + """</span>
<span class="tag">Objectif: """ + str(profile['financial_goal']) + """ EUR/mois</span>
</div></div>
<article class="result-content" id="content">"""

        # Stream Claude response chunks
        for chunk in generate_business_plan_stream(profile):
            safe = chunk.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            yield safe

        yield """</article>
<div class="result-actions no-print" style="margin-top:32px;display:flex;justify-content:center;gap:12px">
<button onclick="window.print()" class="btn btn-primary">Telecharger en PDF</button>
<a href="/" class="btn btn-outline">Generer un autre plan</a></div>
</main>
<footer class="footer"><p>AI Business Generator &mdash; Propulse par Claude AI</p></footer>
<script>
var el = document.getElementById('content');
var raw = el.textContent;
el.innerHTML = marked.parse(raw);
</script></body></html>"""

    return Response(stream_with_context(stream_page()), content_type="text/html")


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


@app.route("/test-api")
def test_api():
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
