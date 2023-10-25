import asyncio
import datetime

import aiohttp
import requests
from more_itertools import chunked

from models import Session, SwapiPeople, Base, engine
from my_lib import get_param, get_id

MAX_CHUNK_SIZE = 10
KEYS_LIST = ["birth_year", "eye_color", "gender" "hair_color", "height", "homeworld", "mass", "name", "skin_color"]
PARAMS = {"films": "title", "vehicles": "name", "starships": "name", "species": "name"}


async def get_people(people_id):
    session = aiohttp.ClientSession()
    response = await session.get(f'https://swapi.dev/api/people/{people_id}')
    json_data = await response.json()
    await session.close()
    return json_data


async def insert_to_db(people_json_list):
    async with Session() as session:
        swapi_people_list = []
        for json_data in people_json_list:
            person = dict()
            for key, val in json_data:
                if key in KEYS_LIST:
                    person[key] = val
            person = get_param(json_data, person)
            person["person_id"] = get_id(json_data)
            swapi_people_list.append(SwapiPeople(**person))

        session.add_all(swapi_people_list)
        await session.commit()


async def main():

    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    for ids_chunk in chunked(range(1, 91), MAX_CHUNK_SIZE):

        get_people_coros = [get_people(person_id) for person_id in ids_chunk]

        bundle = await asyncio.gather(*get_people_coros)

        asyncio.create_task(insert_to_db(bundle))

    current_task = asyncio.current_task()
    tasks_sets = asyncio.all_tasks()
    tasks_sets.remove(current_task)

    await asyncio.gather(*tasks_sets)

    await engine.dispose()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())    # точка входа
    print(datetime.datetime.now() - start)
