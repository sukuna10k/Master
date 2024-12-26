from pyrogram import Client, filters
from imdb import IMDb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialisation IMDb
ia = IMDb()

# Commande /imdb
@Client.on_message(filters.command("imdb"))
async def search_imdb(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Veuillez fournir un mot-clé ou un nom valide.\nExemple : /imdb [nom du film/série]")
        return

    query = message.text.split(" ", 1)[1]

    await message.reply("🔎 Recherche en cours... Veuillez patienter.")
    
    try:
        search_results = ia.search_movie(query)
        
        if not search_results:
            await message.reply("❌ Aucun résultat trouvé.")
            return

        # Créer une liste de boutons pour chaque résultat
        buttons = []
        for result in search_results[:5]:  # Limite à 5 résultats
            buttons.append(
                [InlineKeyboardButton(f"{result['title']} ({result.get('year', 'N/A')})", callback_data=f"imdb_{result.movieID}")]
            )
        
        await message.reply(
            "✅ Résultats trouvés :",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await message.reply(f"❌ Erreur : {e}")

# Gestion des résultats de recherche
@Client.on_callback_query(filters.regex("^imdb_"))
async def fetch_movie_details(client, callback_query):
    movie_id = callback_query.data.split("_")[1]

    try:
        movie = ia.get_movie(movie_id)

        # Texte détaillé
        movie_details = (
            f"🔖 **Titre :** {movie.get('title')}\n"
            f"🎭 **Genre :** {', '.join(movie.get('genres', []))}\n"
            f"🎖 **Note :** {movie.get('rating', 'N/A')}\n"
            f"📆 **Année :** {movie.get('year', 'N/A')}\n\n"
            f"📜 **Synopsis :**\n{movie.get('plot outline', 'Synopsis non disponible')}"
        )

        # Image d'affiche
        poster_url = movie.get('full-size cover url', None)
        
        if poster_url:
            await callback_query.message.reply_photo(photo=poster_url, caption=movie_details)
        else:
            await callback_query.message.reply(movie_details)
    except Exception as e:
        await callback_query.message.edit(f"❌ Erreur : {e}")