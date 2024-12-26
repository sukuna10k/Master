from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube

# Commande /yt
@Client.on_message(filters.command("yt"))
async def download_youtube(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Veuillez fournir un lien YouTube valide.\nExemple : /yt [lien]")
        return

    yt_url = message.text.split(" ", 1)[1]

    try:
        yt_video = YouTube(yt_url)
        title = yt_video.title

        # Boutons de sélection de format
        buttons = [
            [
                InlineKeyboardButton("🫧Original", callback_data=f"yt_original|{yt_url}"),
                InlineKeyboardButton("☀️480p", callback_data=f"yt_480p|{yt_url}"),
                InlineKeyboardButton("🎧MP3", callback_data=f"yt_mp3|{yt_url}")
            ]
        ]
        await message.reply(
            f"🎥 **{title}**\nChoisissez un format de téléchargement :",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await message.reply(f"❌ Erreur : {e}")

# Gestion des téléchargements
@Client.on_callback_query(filters.regex("^yt_"))
async def handle_download(client, callback_query):
    data = callback_query.data.split("|")
    action = data[0]  # yt_original, yt_480p, yt_mp3
    yt_url = data[1]

    await callback_query.message.edit("⏳ Téléchargement en cours... Veuillez patienter.")

    try:
        yt_video = YouTube(yt_url)

        if action == "yt_original":
            video_stream = yt_video.streams.get_highest_resolution()
            file_path = video_stream.download()
            await callback_query.message.reply_video(file_path, caption="🎥 Vidéo en résolution originale")
        elif action == "yt_480p":
            video_stream = yt_video.streams.filter(res="480p").first()
            if not video_stream:
                await callback_query.message.edit("❌ Vidéo 480p non disponible.")
                return
            file_path = video_stream.download()
            await callback_query.message.reply_video(file_path, caption="🎥 Vidéo en 480p")
        elif action == "yt_mp3":
            audio_stream = yt_video.streams.filter(only_audio=True).first()
            file_path = audio_stream.download()
            mp3_path = file_path.replace(".mp4", ".mp3")
            os.rename(file_path, mp3_path)
            await callback_query.message.reply_audio(mp3_path, caption="🎵 Audio MP3")
    except Exception as e:
        await callback_query.message.edit(f"❌ Erreur : {e}")