import requests
from database.trip.conditions import TrafficConditionType
from database.trip.trip import Point
from datetime import timedelta
import math

def total_time(points: list[Point]) -> timedelta:
    total_time = timedelta(minutes=0)
    for point, prev_point in zip(points[1:], points):
        t1 = point.time.replace(tzinfo=None)
        t2 = prev_point.time.replace(tzinfo=None)
        total_time += t1 - t2
    return total_time

def trip_traffic_analysis(points: list[Point]) -> TrafficConditionType:
    starting_point = points[0]
    ending_point = points[-1]
    middle_point = points[math.floor(len(points) / 2)]
    print(f"Starting point: {starting_point.lat}, {starting_point.lng}")
    print(f"Middle point: {middle_point.lat}, {middle_point.lng}")

    api_key = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjFlYzlkMzA5M2RiYjRiMjI5YTVhODQ2MTM1YzVhY2U1IiwiaCI6Im11cm11cjY0In0='

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'
    }

    body = {
        "coordinates": [[starting_point.lng, starting_point.lat], [middle_point.lng, middle_point.lat]]
    }

    # This gets the trip duration when there is no traffic.
    response = requests.post(url, json=body, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        summary = data['features'][0]['properties']['summary']
        first_duration = summary['duration'] / 60
    else:
        print(f"Error {response.status_code}: {response.text}")
        return TrafficConditionType.Light

    second_body = {
        "coordinates": [[middle_point.lng, middle_point.lat], [ending_point.lng, ending_point.lat]]
    }
    response = requests.post(url, json=second_body, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        summary = data['features'][0]['properties']['summary']
        second_duration = summary['duration'] / 60
    else:
        print(f"Error {response.status_code}: {response.text}")
        return TrafficConditionType.Light

    total_duration = first_duration + second_duration
    user_trip_duration = total_time(points).total_seconds() / 60.0

    percentage_increase = (user_trip_duration - total_duration) / user_trip_duration * 100

    if percentage_increase > 30:
        return TrafficConditionType.Heavy
    elif percentage_increase > 20:
        return TrafficConditionType.Moderate
    else:
        return TrafficConditionType.Light
    
