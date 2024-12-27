from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from pymongo import MongoClient
from flask import Flask, jsonify
import asyncio

# Import des gestionnaires supplémentaires
from imdb_handlers import imdb_handler

# Initialisation MongoDB
mongo_client = MongoClient(Config.MONGO_URI)
database = mongo_client[Config.DATABASE_NAME]
users_collection = database["users"]

# Initialisation du bot
bot = Client(
    "MasterAloneBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Sauvegarder un utilisateur dans MongoDB
def save_user(user_id, username, first_name, last_name):
    users_collection.update_one(
        {"_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            }
        },
        upsert=True
    )

# Commande /start
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Sauvegarder l'utilisateur
    save_user(user_id, username, first_name, last_name)

    user_mention = message.from_user.mention
    bot_name = (await client.get_me()).first_name

    # Texte du message
    start_message = (
        f"Sᴀʟᴜᴛ🖐 {user_mention},\n"
        f"Mᴏɴ Nᴏᴍ ᴇsᴛ {bot_name}, Jᴇ ʂυιʂ υɳ 𝚋σƚ α‌ ɱυℓƚιρℓҽ ϝσɳƈƚισɳ, "
        "ᴊᴇ ᴘᴇᴜx ᴇɢᴀʟᴇᴍᴇɴᴛ ᴛᴇʟᴇᴄʜᴀʀɢᴇʀ ᴅᴇs ᴠɪᴅᴇᴏs ʏᴏᴜᴛᴜʙᴇ, ᴘɪɴᴛᴇʀᴇsᴛ, ᴇᴛ ɪɴsᴛᴀɢʀᴀᴍ."
    )

    # Boutons
    buttons = [
        [
            InlineKeyboardButton("⭐️À propos", callback_data="about"),
            InlineKeyboardButton("αɳιɱҽ ƈɾσɯ", url=Config.ANIME_CROW_LINK),
        ]
    ]

    await message.reply_photo(
        photo=Config.START_IMAGE_URL,
        caption=start_message,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Commande /help
@bot.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = (
        "💡 **Commandes disponibles :**\n"
        "/start - Démarrer le bot\n"
        "/help - Voir l'aide\n"
        "/imdb [nom] - Rechercher un film ou série\n"
        "/song [titre] - Rechercher une chanson\n"
        "/yt [lien YouTube] - Télécharger une vidéo YouTube\n"
        "/pint [lien Pinterest] - Télécharger une vidéo Pinterest\n"
        "/inst [lien Instagram] - Télécharger une vidéo Instagram\n"
    )
    await message.reply(help_text)

# Gérer les messages privés envoyés directement au bot
@bot.on_message(filters.private & ~filters.command)
async def direct_message_handler(client, message):
    await message.reply(
        "❌ N'envoyez pas de message directement ici.\n"
        "Envoyez vos demandes sur [@Antiflix_bot](https://t.me/Antiflix_bot).",
        disable_web_page_preview=True
    )

# Serveur HTTP Flask pour Koyeb
app = Flask('')

@app.route('/')
def home():
    return jsonify({"status": "Bot is running!"}), 200

# Lancer Flask et Pyrogram avec asyncio
async def run_flask():
    loop = asyncio.get_event_loop()
    from werkzeug.serving import make_server
    server = make_server("0.0.0.0", 8000, app)
    loop.run_in_executor(None, server.serve_forever)

async def main():
    # Enregistrer le gestionnaire IMDB
    imdb_handler(bot)

    # Démarrer Flask et Pyrogram
    await asyncio.gather(
        bot.start(),
        run_flask()
    )

if __name__ == "__main__":
    asyncio.run(main())
