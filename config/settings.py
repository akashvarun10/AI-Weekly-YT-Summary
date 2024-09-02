import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    def __init__(self):
        if self.MONGODB_URI:
            logger.info("MongoDB URI is set")
        else:
            logger.warning("MongoDB URI is not set")

settings = Settings()

# Attempt to connect to MongoDB
try:
    # We'll assume you're using pymongo to connect
    from pymongo import MongoClient
    client = MongoClient(settings.MONGODB_URI)
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")