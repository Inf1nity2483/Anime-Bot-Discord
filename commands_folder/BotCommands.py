import discord

from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

from commands_folder.commands.search_anime import search_anime
from commands_folder.commands.random_anime import random_anime
from commands_folder.commands.favorite_anime import favorite_anime

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    anime = SlashCommandGroup(
        name="anime",
        description="команды для взаимодействия с аниме"
    )    

    #user_set = user.create_subgroup(name='set', description='user settings')

    @anime.command(name='search', description = 'Поиск аниме по названию')
    async def _search(self, ctx, 
                        query: Option(str, "Введите название аниме",
                            required=True)
                        ):
        await search_anime(ctx, query)
        
    @anime.command(name='random', description = 'Случайное аниме')
    async def _random(self, ctx):
        await random_anime(ctx)

    @anime.command(name='list', descrption='Вывести список избранных аниме')
    async def _list(self, ctx):
        await favorite_anime(ctx)


def setup(bot):
    bot.add_cog(Commands(bot))
