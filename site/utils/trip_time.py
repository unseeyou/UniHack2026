import requests
from datetime import datetime, timedelta

def calculate_day_night_hours(
    start: str, end: str, lat: float, lon: float
) -> tuple[float, float]:
    
    #converts iso 8601 string to datetime
    start = datetime.fromisoformat(start) 
    end = datetime.fromisoformat(end)

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=sunrise,sunset&timezone=Australia/Sydney"
    try:
        response = requests.get(url)
        data = response.json()

        sunset_str = data["daily"]["sunset"][0]
        sunset_time = datetime.strptime(sunset_str, "%Y-%m-%dT%H:%M")

        sunrise_str = data["daily"]["sunrise"][0]
        sunrise_time = datetime.strptime(sunrise_str, "%Y-%m-%dT%H:%M")

        day_minutes = 0
        night_minutes = 0

        current = start

        while current < end:
            if sunrise_time <= current <= sunset_time:
                day_minutes += 1
            else:
                night_minutes += 1
            
            current += timedelta(minutes=1) #same as i++ but with datetime

        day_hours = day_minutes / 60
        night_hours = night_minutes / 60    
        
        return round(day_hours, 1), round(night_hours, 1)


    except Exception as e:
        print(e)
        return "unknown"

    
if __name__ == "__main__":
    print(calculate_day_night_hours("2026-03-13T06:00:00", "2026-03-13T22:00:00", -33.8688, 151.2093))