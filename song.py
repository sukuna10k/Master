from pyrogram import Client, filters
from shazamio import Shazam
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp

# Initialisation de Shazam
shazam = Shazam()

# Commande /song
@Client.on_message(filters.command("song"))
async def search_song(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Veuillez fournir un titre ou un mot-clé valide.\nExemple : /song [titre ou artiste]")
        return

    query = message.text.split(" ", 1)[1]

    await message.reply("🔎 Recherche en cours... Veuillez patienter.")
    
    try:
        results = await shazam.search_track(query)

        if not results["tracks"]["hits"]:
            await message.reply("❌ Aucun résultat trouvé.")
            return

        # Créer une liste de boutons pour chaque résultat
        buttons = []
        for track in results["tracks"]["hits"][:5]:  # Limite à 5 résultats
            title = track["track"]["title"]
            subtitle = track["track"]["subtitle"]
            track_id = track["track"]["key"]

            buttons.append(
                [InlineKeyboardButton(f"{title} - {subtitle}", callback_data=f"song_{track_id}")]
            )
        
        await message.reply(
            "✅ Résultats trouvés :",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await message.reply(f"❌ Erreur : {e}")

# Gestion des résultats de recherche
@Client.on_callback_query(filters.regex("^song_"))
async def fetch_song_details(client, callback_query):
    track_id = callback_query.data.split("_")[1]

    try:
        track = await shazam.get_track_details(track_id)

        # Détails de la chanson
        title = track["title"]
        subtitle = track["subtitle"]
        audio_url = track["hub"]["actions"][1]["uri"]

        # Télécharger l'audio
        async with aiohttp.ClientSession() as session:
            async with session.get(audio_url) as resp:
                with open(f"{title}.mp3", "wb") as f:
                    f.write(await resp.read())

        await callback_query.message.reply_audio(
            audio=f"{title}.mp3",
            caption=f"🎵 **Titre :** {title}\n🎤 **Artiste :** {subtitle}\n\nMerci d'avoir utilisé @Master_Alone_bot !"
        )
    except Exception as e:
        await callback_query.message.edit(f"❌ Erreur : {e}")