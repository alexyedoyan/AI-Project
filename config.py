import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8574982407:AAFgTfgYfe90WAYH3HSq-VkDWJeWO5zcbJw")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "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")

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан в .env файле")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY не задан в .env файле")
