import discord

from models import db

from colorutils import random_rgb

async def favorite_anime(ctx):
    user_id = str(ctx.user.id)

    embed = discord.Embed()
    embed.title = 'Ваши избранные аниме'

    if user_id not in db.users or not db.users[user_id]:
        desc = 'Список пуст!'

    else:
        desc = ''
        for index, name_of_anime in enumerate(db.users[user_id]):
            desc += f"{index+1}. {name_of_anime}\n"
    

    embed.description = desc

    embed.color = discord.Color.from_rgb(*random_rgb())

    await ctx.respond(embed=embed)