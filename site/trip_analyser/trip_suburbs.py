import requests
from database.trip.trip import Point



def get_start_end_locations(points: list[Point]) -> str:
    api_key = '69b6142a622ed232090579rdg86e969'
    starting_point = points[0]
    ending_point = points[-1]

    start_end_suburbs = []
    starting_point_link = f'https://geocode.maps.co/reverse?lat={starting_point.lat}&lon={starting_point.lng}&api_key={api_key}'
    ending_point_link = f'https://geocode.maps.co/reverse?lat={ending_point.lat}&lon={ending_point.lng}&api_key={api_key}'
    response = requests.get(starting_point_link)
    data = response.json()
    start_end_suburbs.append(data.get('address').get("suburb"))
    response = requests.get(ending_point_link)
    data = response.json()
    start_end_suburbs.append(data.get('address').get("suburb"))
    
    return " --> ".join(start_end_suburbs)

