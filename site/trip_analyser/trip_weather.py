from flask import app
import requests
from datetime import datetime
from pprint import pprint
from database.trip.conditions import WeatherConditionType

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

def get_trip_weather(date: str, lat: float, long: float) -> WeatherConditionType:
    current_date = datetime.fromisoformat(date).date()
    params = {
        "latitude": lat, "longitude": long,
        "start_date": current_date, "end_date": current_date,
        "daily": "weather_code", "hourly": "temperature_2m,weather_code",
        "timezone": "Australia/Sydney"
    }
    
    try:
        response = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)
        data = response.json()

        hourly_data = data.get('hourly')

        
        for index, time in enumerate(hourly_data.get('time')):
            #Todo: Change this later to use the datetime module
            if time == date[:16]:
                weather_code = hourly_data.get('weather_code')[index]
                return analyze_weather_code(weather_code)        

        return -1
    except Exception as e:
        app.logger.exception(e)
        return -1.0, -1.0
    
    
if __name__ == "__main__":
    pprint(
        get_trip_weather("2026-03-13T10:00:00", -33.8688, 151.2093)
    )

    