import requests
from constants import app

from typing import Literal


def get_road_classification(
    lat, lon
) -> Literal["unsealed", "highway", "main road", "quiet street", "sealed", "unknown"]:
    overpass_url = " https://maps.mail.ru/osm/tools/overpass/api/interpreter"

    # Query finds the nearest 'way' with a 'highway' tag within 20m
    query = f"""
    [out:json];
    way(around:20, {lat}, {lon})[highway];
    out tags;
    """

    try:
        response = requests.post(overpass_url, data={"data": query})
        data = response.json()
        print(data["elements"])

        if not data.get("elements"):
            app.logger.warning("No road found at these coordinates.")
            return "unknown"

        # Get tags from the first matching road element
        tags = data["elements"][0].get("tags", {})
        hw = tags.get("highway", "").lower()
        surface = tags.get("surface", "").lower()

        # 1. Check for Unsealed (Surface takes priority)
        unsealed_terms = [
            "unpaved",
            "gravel",
            "dirt",
            "sand",
            "earth",
            "ground",
            "compacted",
        ]
        if surface in unsealed_terms:
            return "unsealed"

        # 2. Classify by Road Importance/Type
        if hw in ["motorway", "trunk", "motorway_link"]:
            return "highway"

        if hw in ["primary", "secondary", "primary_link", "secondary_link"]:
            return "main road"

        if hw in ["residential", "living_street", "tertiary", "tertiary_link"]:
            return "quiet street"

        # 3. Default to Sealed if it's a known hard surface or a standard road type
        sealed_terms = ["asphalt", "paved", "concrete", "bitumen", "paving_stones"]
        if surface in sealed_terms or hw:
            return "sealed"

        return "unknown"

    except Exception as e:
        app.logger.exception(e)
        return "unknown"


if __name__ == "__main__":
    print(get_road_classification(-33.80434765065589, 151.1862909590549))
