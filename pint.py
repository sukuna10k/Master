from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pinterest_downloader import Pinterest

# Commande /pint
@Client.on_message(filters.command("pint"))
async def download_pinterest_video(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Veuillez fournir un lien Pinterest valide.\nExemple : /pint [lien]")
        return

    pint_url = message.text.split(" ", 1)[1]

    await message.reply("⏳ Téléchargement en cours... Veuillez patienter.")
    
    try:
        pinterest = Pinterest(pint_url)
        video_url = pinterest.video_url()

        # Téléchargement de la vidéo
        await message.reply_video(video_url, caption="🎥 Vidéo téléchargée depuis Pinterest")
    except Exception as e:
        await message.reply(f"❌ Erreur : {e}")