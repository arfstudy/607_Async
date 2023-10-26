import requests

PARAMS = {"films": "title", "vehicles": "name", "starships": "name", "species": "name"}


def get_id(person):
    url = person["url"]
    u_len = len(url)
    corr = 0
    while url[:u_len - corr].endswith('/'):
        corr += 1
    p_start = url[:u_len - corr].rfind('/')
    number = url[p_start + 1: u_len - corr]
    if number.isnumeric():
        return number
    return number + '-не_число'


def get_param(json_data, single):
    for key, val in PARAMS.items():
        value = []
        for address in json_data[key]:
            res = requests.get(address).json()
            value.append(res[val])
        single[key] = ", ".join(value)
    return single
