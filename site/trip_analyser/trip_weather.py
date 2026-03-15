from constants import app
import requests
from datetime import datetime
from database.trip.conditions import WeatherConditionType
from database.trip.trip import Point


def analyze_weather_code(weather_code: int) -> WeatherConditionType:
    FINE_CODES = {0, 1, 2, 3}
    RAIN_CODES = {51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99}
    SNOW_CODES = {71, 73, 75, 77, 85, 86}
    ICY_CODES = {56, 57, 66, 67}
    FOG_CODES = {45, 48}

    if weather_code in FINE_CODES:
        return WeatherConditionType.Fine
    elif weather_code in RAIN_CODES:
        return WeatherConditionType.Raining
    elif weather_code in SNOW_CODES:
        return WeatherConditionType.Snow
    elif weather_code in ICY_CODES:
        return WeatherConditionType.Icy
    elif weather_code in FOG_CODES:
        return WeatherConditionType.Fog


def get_weather_conditions(points: list[Point]):
    return set(map(get_point_weather, points))


def get_point_weather(point: Point) -> WeatherConditionType:
    params = {
        "latitude": point.lat,
        "longitude": point.lng,
        "start_date": point.time.date(),
        "end_date": point.time.date(),
        "daily": "weather_code",
        "hourly": "temperature_2m,weather_code",
        "timezone": "Australia/Sydney",
    }

    try:
        response = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)
        data = response.json()

        hourly_data = data.get("hourly")

        for index, time in enumerate(hourly_data.get("time")):
            time = datetime.fromisoformat(time)
            if time >= point.time:
                weather_code = hourly_data.get("weather_code")[index]
                return analyze_weather_code(weather_code)

        return WeatherConditionType.Fine
    except Exception as e:
        app.logger.exception(e)
        return WeatherConditionType.Fine
