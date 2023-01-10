import discord

from bs4 import BeautifulSoup
from anime import AnimeBot
from models import Anime, db

from colorutils import random_rgb

class SearchAnime(discord.ui.View):
    def __init__(self, query) -> None:
        super().__init__(timeout=None)
        self.index = 0
        self.query = query

    async def get_anime_count(self):
        html = await AnimeBot.search(self.query)

        soup = BeautifulSoup(html, 'lxml')

        soup = soup.find_all('div', class_='animes-grid-item col-6 col-sm-6 col-md-4 col-lg-3 col-xl-2 col-ul-2')

        self.count_anime = len(soup)

    async def loading(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
                                    content='**Loading...**',
                                    embed=None,
                                    view=None
                                    )

    async def saving(self, interaction: discord.Interaction, embed):
        await interaction.edit_original_response(
                                    content='',
                                    embed=embed,
                                    view=self
                                    )
    
    async def check(self):
        if self.index == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        if self.index == self.count_anime-1:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

    async def parse(self):
        html = await AnimeBot.search(self.query)

        soup = BeautifulSoup(html, 'lxml')

        soup = soup.find_all('div', class_='animes-grid-item col-6 col-sm-6 col-md-4 col-lg-3 col-xl-2 col-ul-2')

        self.count_anime = len(soup)

        assert len(soup) != 0, "Аниме не найдено!"

        soup = soup[self.index]

        title = soup.find('div', class_='h5 font-weight-normal mb-2 card-title text-truncate').find('a').text
        href = soup.find('div', class_='h5 font-weight-normal mb-2 card-title text-truncate').find('a').get('href')
        image = soup.find('div', class_='anime-grid-lazy lazy').get('data-original')
        rating = soup.find('div', class_='p-rate-flag__text')
        if rating is not None:
            rating = rating.text
        year = soup.find('span', class_='anime-year').text

        self.title = title

        embed = discord.Embed()
        embed.color = discord.Color.from_rgb(*random_rgb())
        embed.title = title
        embed.url = href

        embed.add_field(
            name='Рейтинг',
            value=rating
        )

        embed.add_field(
            name='Год выхода',
            value=year
        )

        embed.set_image(url=image)

        return embed

    @discord.ui.button(label="←", row=0, style=discord.ButtonStyle.red, custom_id='button-1')
    async def first_button_callback(self, button, interaction):
        await self.loading(interaction)
        self.index -= 1
        await self.check()
        embed = await self.parse()
        await self.saving(interaction, embed)

    @discord.ui.button(label="→", row=0, style=discord.ButtonStyle.red, custom_id='button-2')
    async def second_button_callback(self, button, interaction):
        await self.loading(interaction)
        self.index += 1
        await self.check()
        embed = await self.parse()
        await self.saving(interaction, embed)

    @discord.ui.button(label='⭐', row=1, style=discord.ButtonStyle.red, custom_id='button-3')
    async def third_button_callback(self, button, interaction):
        user_id = str(interaction.user.id)

        if user_id not in db.users:
            db.users[user_id] = []

        status = await db.add_anime_to_favorite(user_id, self.title)

        embed = discord.Embed(
            title="Готово!",
            description=f"Аниме `{self.title}` {status}!",
            color=discord.Color.from_rgb(*random_rgb())
        )

        await interaction.response.send_message(
            interaction.user.mention,
            embed=embed)
        
        
async def search_anime(ctx, query):
    view = SearchAnime(query)
    await view.get_anime_count()
    await view.check()

    embed = await view.parse()
    await ctx.respond(embed=embed, view=view)