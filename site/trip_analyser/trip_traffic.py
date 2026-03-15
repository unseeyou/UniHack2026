import requests
from database.trip.conditions import TrafficConditionType
from database.trip.trip import Point

# idk what user trip duration is but like i'm gonna assume it's a float of minutes
def get_trip_traffic(starting_point: Point, ending_point: Point, user_trip_duration: float) -> TrafficConditionType:
    #!!!!!!!!!!!!!!!!
    # TODO: MOVE KEY TO CONSTANTS !!!!!!!!!!!!!!!!
    api_key = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjFlYzlkMzA5M2RiYjRiMjI5YTVhODQ2MTM1YzVhY2U1IiwiaCI6Im11cm11cjY0In0='


    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'
    }

    body = {
        "coordinates": [[starting_point.lng, starting_point.lat], [starting_point.lng, starting_point.lat]]
    }

    # This gets the trip duration when there is no traffic.
    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        summary = data['features'][0]['properties']['summary']

        duration = summary['duration'] / 60
        percentage_increase = duration / user_trip_duration * 100

        if percentage_increase > 30:
            return TrafficConditionType.Heavy
        elif percentage_increase > 20:
            return TrafficConditionType.Moderate
        else:
            return TrafficConditionType.Light
    else:
        print(f"Error {response.status_code}: {response.text}")
        return TrafficConditionType.Light

