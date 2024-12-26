import os
from urllib.parse import quote_plus  # Pour encoder les caractères spéciaux dans l'URI MongoDB

class Config:
    # Telegram API
    API_ID = int(os.getenv("API_ID", "24817837"))  # Remplacez par votre API_ID Telegram
    API_HASH = os.getenv("API_HASH", "acd9f0cc6beb08ce59383cf250052686")  # Remplacez par votre API_HASH Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7887721284:AAGzvi6l2gNt8vuLUJ3PZybqDtl4OhRgz3Y")  # Token de votre bot

    # Forcing subscription
    FORCE_SUB_CHANNEL_1 = os.getenv("FORCE_SUB_CHANNEL_1", "@Otakukingcey1")  # Premier canal
    FORCE_SUB_CHANNEL_2 = os.getenv("FORCE_SUB_CHANNEL_2", "@AntiFlix_A")  # Deuxième canal

    # MongoDB Configuration
    MONGO_USERNAME = os.getenv("MONGO_USERNAME", "lucia")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "@Marsh_mello_bot")  # Mot de passe avec caractères spéciaux
    MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "lucia.bwnrs.mongodb.net")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "lucia")  # Nom de la base de données MongoDB

    # Construire une URI MongoDB sécurisée
    MONGO_URI = f"mongodb+srv://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=lucia"

    # API Keys
    OMDB_API_KEY = os.getenv("OMDB_API_KEY", "34960695")  # Clé API pour OMDB
    SHAZAM_API_KEY = os.getenv("SHAZAM_API_KEY", "1156fd018cmsh121aea6464d631dp148b95jsnf0218bff9a18")  # Clé API pour Shazam

    # Configuration pour le texte et les boutons
    START_IMAGE_URL = "https://envs.sh/JXL.jpg"
    ANIME_CROW_LINK = "https://t.me/+wm74AQeTKOZlNTc0"

    # ID propriétaire
    OWNER_ID = int(os.getenv("OWNER_ID", "7428552084"))  # ID de l'administrateur principal