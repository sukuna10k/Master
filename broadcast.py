from pyrogram import Client, filters
from config import Config
from pymongo import MongoClient
from pyrogram.errors import FloodWait
import time

# Connexion à MongoDB
mongo_client = MongoClient(Config.MONGO_URI)
database = mongo_client[Config.DATABASE_NAME]
users_collection = database["users"]

# Commande /broadcast (uniquement pour l'administrateur)
@Client.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID))
async def broadcast_message(client, message):
    if not message.reply_to_message:
        await message.reply("❌ Répondez à un message pour le diffuser à tous les utilisateurs.")
        return

    broadcast_msg = message.reply_to_message
    total_users = users_collection.count_documents({})
    sent_count = 0

    await message.reply(f"🔄 Diffusion en cours... Total d'utilisateurs : {total_users}")

    # Diffuser à tous les utilisateurs
    for user in users_collection.find():
        try:
            await broadcast_msg.copy(chat_id=user["_id"])
            sent_count += 1
        except FloodWait as e:
            time.sleep(e.value)  # Pause pour éviter les limitations de Telegram
        except Exception as ex:
            print(f"Erreur pour l'utilisateur {user['_id']}: {ex}")

    await message.reply(f"✅ Diffusion terminée. Messages envoyés : {sent_count}/{total_users}")