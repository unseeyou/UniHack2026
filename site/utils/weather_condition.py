import requests


def get_weather_condition(lat: float, lon: float) -> str:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=weathercode"

    try:
        response = requests.get(url)
        data = response.json()
        code = data["current"]["weathercode"]

        if code in [0, 1, 2, 3]:
            return "fine"
        elif code in [45, 48]:
            return "fog"
        elif (
            code in [51, 53, 55, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99]
            or code > 99
        ):
            return "rain"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "snow"
        else:
            return "unkown"

    except Exception as e:
        print(e)
        return "unkown"


if __name__ == "__main__":
    print(get_weather_condition(-33.8688, 151.2093))
