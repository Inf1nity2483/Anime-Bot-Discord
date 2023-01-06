import discord

from models import db

from colorutils import random_rgb

async def send_anime_updated(news, bot):
    for anime in news:
        name_of_anime = news[anime]['title']
        if news[anime]['title'] not in db.favorite_anime: continue
        for user in db.favorite_anime[name_of_anime]:
            user = await bot.fetch_user(user)
            embed = discord.Embed()
            embed.title = anime
            embed.description = 'Вышла новая серия аниме!'
            embed.url = news[anime]['href']
            embed.set_thumbnail(url=news[anime]['image'])
            embed.color=discord.Color.from_rgb(*random_rgb())
            await user.send(embed=embed)
