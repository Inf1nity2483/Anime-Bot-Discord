import aiohttp

class Anime:
    def __init__(self) -> None:
        self.url = 'https://animego.org/'
        self.search_url = 'search/anime?q='
        self.random_url = 'anime/random'
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    async def parse(self, url: str='') -> str:
        session = aiohttp.ClientSession()
        async with session.get(self.url+url, headers=self.user_agent) as response:
            text = await response.text()
        await session.close()
        return text

    async def search(self, query: str) -> str:
        return await self.parse(self.search_url+'%20'.join(query.split()))

    async def random(self) -> str:
        return await self.parse(self.random_url)

AnimeBot = Anime()