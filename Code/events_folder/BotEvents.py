import discord
from discord.ext import commands, tasks

from models import db

from colorutils import random_rgb

from events_folder.parse import get_news
from events_folder.send_anime_updated import send_anime_updated as send_update

class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.data = []
        self.check_update.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Авторизация:', self.bot.user)

    @tasks.loop(minutes=5)
    async def check_update(self):
        news = await get_news()
        news = await db.check_anime_in_history(news)
        await send_update(news, self.bot)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        embed = discord.Embed()
        embed.title = 'Ошибка!'
        embed.description = str(error.original)
        embed.color = discord.Color.from_rgb(*random_rgb())

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))