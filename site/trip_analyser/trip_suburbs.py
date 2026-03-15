import requests
from database.trip.trip import Point

def get_start_end_locations(starting_point: Point, ending_point: Point):
    #TODO: PUT THIS INTO CONSTANTS!!!!!!!!!!!! PLEASE SOMEONE DO IT  :(((
    api_key = '69b6142a622ed232090579rdg86e969'
    
    start_end_suburbs = []
    starting_point_link = f'https://geocode.maps.co/reverse?lat={starting_point.lat}&lon={starting_point.lng}&api_key={api_key}'
    ending_point_link = f'https://geocode.maps.co/reverse?lat={ending_point.lat}&lon={ending_point.lng}&api_key={api_key}'
    response = requests.get(starting_point_link)
    data = response.json()
    start_end_suburbs[0] = data.get('address').get("suburb")
    response = requests.get(ending_point_link)
    data = response.json()
    start_end_suburbs[1] = data.get('address').get("suburb")
    
    return start_end_suburbs

