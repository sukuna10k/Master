from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from pymongo import MongoClient

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
        "𝙹𝙴 𝙿𝙴𝚄𝚇 ᴠᴏᴜs ғᴏᴜʀɴɪʀ ᴅᴇs ᴅᴏɴɴᴇᴇs ᴅᴇ ғɪʟᴍ, sᴇʀɪᴇs ᴇᴛ ᴀɴɪᴍᴇs. 😏\n\n"
        "ᴊᴇ ᴘᴇᴜx ᴇɢᴀʟᴇᴍᴇɴᴛ ᴛᴇʟᴇᴄʜᴀʀɢᴇʀ ᴅᴇs ᴠɪᴅᴇᴏs ʏᴏᴜᴛᴜʙᴇ, ᴘɪɴᴛᴇʀᴇsᴛ, ᴇᴛ ɪɴsᴛᴀɢʀᴀᴍ ᴊᴜsᴛᴇ ᴇɴ ᴍᴇɴᴠᴏʏᴀɴᴛ ʟᴇ ʟɪᴇɴ. "
        "ᴄʟɪᴄᴋ sᴜʀ /help ᴇᴛ ᴠᴏɪs ᴍᴇs ғᴏɴᴄᴛɪᴏɴɴᴀʟɪᴛᴇs."
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

# Gestion du bouton "À propos"
@bot.on_callback_query(filters.regex("about"))
async def about_callback(client, callback_query):
    bot_mention = (await client.get_me()).mention

    # Texte du message "À propos"
    about_message = (
        "╭───[🔅KGC🔅]────⍟\n"
        "│\n"
        f"├🔸🤖 Moɴ ɴoм: {bot_mention}\n"
        "│\n"
        "├🔸📝 Lαɴɢυαɢe: Ƥутнση3\n"
        "│\n"
        "├🔹📚 Bιвlιoтнe‌qυe: Pчrogrαm\n"
        "│\n"
        "├🔹📡 He‌вerɢe‌ ѕυr: ANTIFLIX\n"
        "│\n"
        "├🔸👨‍💻 De‌veloppeυr: 🇰ιηg¢єу\n"
        "│\n"
        "├🔸🔔 Mα Cнαι‌ɴe: AntiFlix Actu\n"
        "│\n"
        "╰─────────[ 😎 ]────────⍟"
    )

    # Bouton de retour
    buttons = [[InlineKeyboardButton("⪻Backメ", callback_data="back_to_start")]]
    
    # Réponse au callback
    await callback_query.message.edit_text(
        text=about_message,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Gestion du bouton de retour au démarrage
@bot.on_callback_query(filters.regex("back_to_start"))
async def back_to_start(client, callback_query):
    user_mention = callback_query.from_user.mention
    bot_name = (await client.get_me()).first_name

    # Texte du message
    start_message = (
        f"Sᴀʟᴜᴛ🖐 {user_mention},\n"
        f"Mᴏɴ Nᴏᴍ ᴇsᴛ {bot_name}, Jᴇ ʂυιʂ υɳ 𝚋σƚ α‌ ɱυℓƚιρℓҽ ϝσɳƈƚισɳ, "
        "𝙹𝙴 𝙿𝙴ᴜ𝚇 ᴠᴏᴜs ғᴏᴜʀɴɪʀ ᴅᴇs ᴅᴏɴɴᴇᴇs ᴅᴇ ғɪʟᴍ, sᴇʀɪᴇs ᴇᴛ ᴀɴɪᴍᴇs. 😏\n\n"
        "ᴊᴇ ᴘᴇᴜx ᴇɢᴀʟᴇᴍᴇɴᴛ ᴛᴇʟᴇᴄʜᴀʀɢᴇʀ ᴅᴇs ᴠɪᴅᴇᴏs ʏᴏᴜᴛᴜʙᴇ, ᴘɪɴᴛᴇʀᴇsᴛ, ᴇᴛ ɪɴsᴛᴀɢʀᴀᴍ ᴊᴜsᴛᴇ ᴇɴ ᴍᴇɴᴠᴏʏᴀɴᴛ ʟᴇ ʟɪᴇɴ. "
        "ᴄʟɪᴄᴋ sᴜʀ /help ᴇᴛ ᴠᴏɪs ᴍᴇs ғᴏɴᴄᴛɪᴏɴɴᴀʟɪᴛᴇs."
    )

    # Boutons
    buttons = [
        [
            InlineKeyboardButton("⭐️À propos", callback_data="about"),
            InlineKeyboardButton("αɳιɱҽ ƈɾσɯ", url=Config.ANIME_CROW_LINK),
        ]
    ]

    await callback_query.message.edit_text(
        text=start_message,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Commande /help
@bot.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = (
        "💡 **Commandes disponibles :**\n"
        "/start - Démarrer le bot\n"
        "/imdb [nom] - Rechercher un film ou série\n"
        "/song [titre] - Rechercher une chanson\n"
        "/yt [lien YouTube] - Télécharger une vidéo YouTube\n"
        "/pint [lien Pinterest] - Télécharger une vidéo Pinterest\n"
        "/inst [lien Instagram] - Télécharger une vidéo Instagram\n"
    )
    await message.reply(help_text)

# Lancer le bot
if __name__ == "__main__":
    bot.run()