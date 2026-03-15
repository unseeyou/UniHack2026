import requests
from datetime import datetime, timedelta
from pytz import timezone, utc
from constants import app
from database.trip.trip import Point


def calculate_day_night_time(
    points: list[Point]
) -> tuple[float, float]:
    day_time = timedelta()
    night_time = timedelta()

    for point, prev_point in zip(points[1:], points):
        if is_day(point):
            day_time += point.time - prev_point.time
        else:
            night_time += point.time - prev_point.time

    return day_time, night_time

    
def is_day(point: Point):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={point.lat}&longitude={point.lng}&daily=sunrise,sunset&timezone=Australia/Sydney"

    try:
        response = requests.get(url)
        data = response.json()

        sunset_str = data["daily"]["sunset"][0]
        sunset_time = datetime.strptime(sunset_str, "%Y-%m-%dT%H:%M").astimezone(timezone("Australia/Sydney"))

        sunrise_str = data["daily"]["sunrise"][0]
        sunrise_time = datetime.strptime(sunrise_str, "%Y-%m-%dT%H:%M").astimezone(timezone("Australia/Sydney"))

        return sunrise_time <= point.time.astimezone(utc) <= sunset_time
    except Exception as e:
        app.logger.exception(e)
        return True

