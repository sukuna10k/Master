import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import instaloader

# Initialisation d'Instaloader
insta_loader = instaloader.Instaloader()

# Commande /inst
@Client.on_message(filters.command("inst"))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Veuillez fournir un lien Instagram valide.\nExemple : /inst [lien]")
        return

    insta_url = message.text.split(" ", 1)[1]

    await message.reply("⏳ Téléchargement en cours... Veuillez patienter.")
    
    try:
        # Téléchargement de la vidéo Instagram
        post = instaloader.Post.from_shortcode(insta_loader.context, insta_url.split("/")[-2])
        video_url = post.video_url

        # Téléchargement et envoi de la vidéo
        await message.reply_video(video_url, caption="🎥 Vidéo téléchargée depuis Instagram")
    except Exception as e:
        await message.reply(f"❌ Erreur : {e}")