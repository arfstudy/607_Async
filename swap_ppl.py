import asyncio
import datetime

import aiohttp
import requests

PARAMS = {"films": "title", "vehicles": "name", "starships": "name", "species": "name"}


async def get_people(people_id):
    """ Оформим, чтобы функция get_people() могла работать асинхронно. """
    session = aiohttp.ClientSession()
    #
    print(f'{people_id=}')                  # Для теста
    response = await session.get(f'https://swapi.dev/api/people/{people_id}')
    print(f'{people_id=}, {response=}')     # Для теста
    json_data = await response.json()
    print(f'{people_id=}, {json_data=}')    # Для теста
    await session.close()
    print(f'{people_id=} - session closed') # Для теста
    #
    return json_data


def get_param(single):
    for key, val in PARAMS.items():
        value = []
        for address in single[key]:
            res = requests.get(address).json()
            value.append(res[val])
        single[key] = ", ".join(value)
    return single


async def main():

    # person = get_param(person)

    person_1 = get_people(1)
    person_2 = get_people(2)
    person_3 = get_people(3)
    person_4 = get_people(4)
    print(person_1, person_2, person_3, person_4)


start = datetime.datetime.now()
asyncio.run(main())    # точка входа
print(datetime.datetime.now() - start)
