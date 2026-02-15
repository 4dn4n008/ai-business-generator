import markdown
from weasyprint import HTML

PDF_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.7;
        color: #1a1a2e;
        max-width: 800px;
        margin: 0 auto;
        padding: 40px;
    }}
    h1 {{
        color: #6c5ce7;
        border-bottom: 3px solid #6c5ce7;
        padding-bottom: 10px;
        font-size: 28px;
    }}
    h2 {{
        color: #6c5ce7;
        margin-top: 30px;
        font-size: 20px;
    }}
    .header {{
        text-align: center;
        margin-bottom: 40px;
        padding: 30px;
        background: linear-gradient(135deg, #6c5ce7, #a855f7);
        color: white;
        border-radius: 12px;
    }}
    .header h1 {{
        color: white;
        border: none;
        margin: 0;
        font-size: 32px;
    }}
    .header p {{
        margin: 5px 0 0;
        opacity: 0.9;
    }}
    .profile-box {{
        background: #f8f9ff;
        border: 1px solid #e0e0ff;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 30px;
    }}
    ul, ol {{
        padding-left: 20px;
    }}
    li {{
        margin-bottom: 4px;
    }}
    strong {{
        color: #6c5ce7;
    }}
</style>
</head>
<body>
    <div class="header">
        <h1>AI Business Generator</h1>
        <p>Plan Business Personnalise</p>
    </div>
    <div class="profile-box">
        <h2>Profil</h2>
        <ul>
            <li><strong>Age:</strong> {age} ans</li>
            <li><strong>Budget:</strong> {budget} EUR</li>
            <li><strong>Competences:</strong> {skills}</li>
            <li><strong>Temps/semaine:</strong> {available_time}h</li>
            <li><strong>Pays:</strong> {country}</li>
            <li><strong>Objectif:</strong> {financial_goal} EUR/mois</li>
        </ul>
    </div>
    {content}
</body>
</html>"""


def generate_pdf(result: str, profile: dict) -> bytes:
    html_content = markdown.markdown(result, extensions=["tables", "fenced_code"])
    full_html = PDF_TEMPLATE.format(
        content=html_content,
        age=profile.get("age", ""),
        budget=profile.get("budget", ""),
        skills=profile.get("skills", ""),
        available_time=profile.get("available_time", ""),
        country=profile.get("country", ""),
        financial_goal=profile.get("financial_goal", ""),
    )
    return HTML(string=full_html).write_pdf()
