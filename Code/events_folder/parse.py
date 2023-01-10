import discord
import asyncio

from bs4 import BeautifulSoup
from anime import AnimeBot

async def get_news():
    html = await AnimeBot.parse()

    soups = BeautifulSoup(html, 'lxml')

    news = {}

    soups = soups.find('div', class_='last-update') 
    soups = soups.find('div', class_='list-group')
    
    for soup in soups.find_all('div', tabindex='-1'):
        if soup.find('div', class_='text-gray-dark-6').text == '(Субтитры)': continue

        title = soup.find('span', class_='last-update-title font-weight-600').text
        series = soup.find('div', class_='font-weight-600 text-truncate').text
        href = soup.get('onclick').split("'")[-2]
        image = soup.find('div', class_='img-square lazy br-50').get('style').split('(')[-1][:-2]

        full_title = title+' - '+series

        news[full_title] = {}
        news[full_title]['title'] = title
        news[full_title]['series'] = series
        news[full_title]['href'] = AnimeBot.url + href
        news[full_title]['image'] = image

    return news
