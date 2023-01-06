import discord

from bs4 import BeautifulSoup
from anime import AnimeBot

from colorutils import random_rgb

async def random_anime(ctx):
    html = await AnimeBot.random()

    soup = BeautifulSoup(html, 'lxml')

    title = soup.find('div', class_='anime-title').find('h1').text
    href = soup.find('meta', property='og:url').get('content')
    image = soup.find('div', class_='anime-poster position-relative cursor-pointer').find('img').get('srcset').split()[0]

    embed = discord.Embed()

    embed.title = title
    embed.url = href
    embed.color = discord.Color.from_rgb(*random_rgb())

    embed.set_image(url=image)
    
    await ctx.respond(embed=embed)