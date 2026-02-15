import sys
import os
from flask import Flask, render_template, request, session, redirect, url_for
from config import Config
from services.claude_service import generate_business_plan
from utils.rate_limiter import can_generate, increment_usage

# Fix paths for PyInstaller
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

    result = generate_business_plan(profile)
    if result is None:
        return render_template("index.html", error="Erreur lors de la generation. Verifiez votre cle API.")

    increment_usage(session)

    return render_template("result.html", result=result, profile=profile)


@app.route("/paywall")
def paywall():
    return render_template("paywall.html")


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
