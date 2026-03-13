import requests

OVERPASS = "https://overpass.private.coffee/api/interpreter?&data="


def from_name(road_name: str) -> str:
    with requests.Session() as s:
        response = s.get(f'{OVERPASS}node["name"~"{road_name}"];out;')
    return response.text


print(from_name("3 barton road artarmon sydney australia"))
