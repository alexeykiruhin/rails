import aiohttp
import json


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_code(station_name):
    # url = f'https://online.freicon.ru/v1/stations' \
    #       f'?page=1' \
    #       f'&per_page=1' \
    #       f'&code=' \
    #       f'&name={station_name}' \
    #       f'&railwayId=0' \
    #       f'&typeId=0'

    url = 'https://suggests.rasp.yandex.net/all_suggests' \
          '?client_city=213' \
          '&field=from' \
          '&format=old' \
          '&lang=ru' \
          '&national_version=ru' \
          '&other_point=s9601782' \
          f'&part={station_name}'

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        html_json = json.loads(html)
        stations = [s for s in html_json[1] if(s[2][:2] == 'пл')]
        # print(stations)

    return stations
