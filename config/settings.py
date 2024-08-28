import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = 587
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

settings = Settings()