import os
import sys
from dotenv import load_dotenv

# When running as .exe, look for .env next to the executable
if getattr(sys, 'frozen', False):
    env_path = os.path.join(os.path.dirname(sys.executable), '.env')
else:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

load_dotenv(env_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MAX_FREE_GENERATIONS = 1
    CLAUDE_MODEL = "claude-haiku-4-5-20251001"
    CLAUDE_MAX_TOKENS = 4000
