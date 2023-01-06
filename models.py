import json
import asyncio

class Anime:
    def __init__(self, 
            name: str, 
            rating: float=None, 
            image: str=None,
            year: str=None,
            series: str=None,
            genre: str=None) -> None:
        self.name = name
        self.rating = rating
        self.image = image
        self.year = year
        self.series = series
        self.genre = genre

class DataBase:
    def __init__(self) -> None:
        self.path = 'data\main.json'

        self.users = {}
        self.favorite_anime = {}
        self.sended_anime = []

    def create_file(self):
        data = {
            'users': {},
            'favorite_anime': {},
            'sended_anime': []
        }
        with open(self.path, 'w') as outfile:
            json.dump(data, outfile)

    def load(self):
        try:
            with open(self.path) as json_file:
                data = json.load(json_file)

            self.favorite_anime = data['favorite_anime']
            self.users = data['users']
            self.sended_anime = data['sended_anime']

        except FileNotFoundError:
            self.create_file()

    async def check_anime_in_history(self, animes):
        checked = {}
        for anime in animes:
            if anime in self.sended_anime: continue
            self.sended_anime.append(anime)
            checked[anime] = animes[anime]
        await self.save()
        return checked
    
    async def add_anime_to_favorite(self, user_id, anime_title):
        if user_id not in self.users:
            self.users[user_id] = []

        if anime_title not in self.favorite_anime:
            self.favorite_anime[anime_title] = []

        if anime_title not in self.users[user_id]:
            self.users[user_id].append(anime_title)
            self.favorite_anime[anime_title].append(user_id)
            status = 'успешно добавлено в избранное'

        elif anime_title in self.users[user_id]:
            self.users[user_id].remove(anime_title)
            self.favorite_anime[anime_title].remove(user_id)
            status = 'успешно удалено из избранного'

        await self.save()

        return status

    async def save(self):
        data = {
            'users': self.users,
            'favorite_anime': self.favorite_anime,
            'sended_anime': self.sended_anime
        }
        with open(self.path, 'w') as outfile:
            json.dump(data, outfile)

db = DataBase()
db.load()