import aiohttp

class Anime:
    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()
        self.url = 'https://animego.org/'
        self.search_url = 'search/anime?q='
        self.random_url = 'anime/random'

    async def parse(self, url: str='') -> str:
        async with self.session.get(self.url+url) as response:
            return await response.text()

    async def search(self, query: str) -> str:
        return await self.parse(self.search_url+'%20'.join(query.split()))

    async def random(self) -> str:
        return await self.parse(self.random_url)

AnimeBot = Anime()