import sys
import os
import webbrowser
import threading

# Fixer le chemin pour PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    os.chdir(BASE_DIR)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ['BASE_DIR'] = BASE_DIR

from app import app

def open_browser():
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    print("=" * 50)
    print("  AI Business Generator")
    print("  Ouvre ton navigateur sur http://localhost:5000")
    print("  Pour arreter : ferme cette fenetre")
    print("=" * 50)
    app.run(host="127.0.0.1", port=5000, debug=False)
