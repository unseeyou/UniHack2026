import requests
import time

from constants import app
from database.trip.trip import Point
from database.trip.conditions import RoadConditionType


def get_road_conditions(points: list[Point]) -> set[RoadConditionType]:
    road_conditions = set()

    points = points[:: max(1, len(points) // 10)]  # Sample up to 10 points for efficiency

    for point in points:
        road_conditions = road_conditions.union(get_point_road_conditions(point))
        time.sleep(1)

    return road_conditions


def get_point_road_conditions(point: Point) -> set[RoadConditionType]:
    overpass_url = "https://maps.mail.ru/osm/tools/overpass/api/interpreter" # "https://overpass.thepyes.au/api/interpreter"
    # Query finds the nearest 'way' with a 'highway' tag within 20m
    query = f"""
    [out:json][timeout:10];
    way(around:20, {point.lat}, {point.lng})[highway];
    out tags;
    """

    user_agent = "RoadAnalyser/0.1 (+https://test.unseeyou.com; contact@unseeyou.com)"

    try:
        response = requests.post(overpass_url, data={"data": query}, headers={"User-Agent": user_agent})
        data = response.json()
    except Exception as e:
        app.logger.exception(e)
        print(response.content)
        return set()

    print(data)
    if "<html>" in response.text:
        return set()

    print(response.content)
    print(data)

    # First element is closest element
    try:
        tags = data["elements"][0].get("tags", {})
    except IndexError:
        app.logger.exception("No tags found")
        return set()

    highway_type = tags.get("highway", "").casefold()
    surface = tags.get("surface", "").casefold()
    num_lanes = int(tags.get("lanes", 1))

    conditions: set[RoadConditionType] = set()

    unsealed_surfaces = set(
        map(
            lambda x: x.casefold(),
            ["unpaved", "gravel", "dirt", "sand", "earth", "ground", "compacted"],
        )
    )
    if surface in unsealed_surfaces:
        conditions.add(RoadConditionType.Unsealed)

    sealed_surfaces = set(
        map(
            lambda x: x.casefold(),
            ["asphalt", "paved", "concrete", "bitumen", "paving_stones"],
        )
    )
    if surface in sealed_surfaces:
        conditions.add(RoadConditionType.Sealed)

    # High way types: ["motorway", "trunk", "motorway_link"]
    main_road_highway_types = set(
        map(
            lambda x: x.casefold(),
            ["primary", "secondary", "primary_link", "secondary_link"],
        )
    )
    if highway_type in main_road_highway_types:
        conditions.add(RoadConditionType.MainRoad)

    quiet_street_highway_types = set(
        map(
            lambda x: x.casefold(),
            ["residential", "living_street", "tertiary", "tertiary_link"],
        )
    )
    if highway_type in quiet_street_highway_types:
        conditions.add(RoadConditionType.QuietStreet)

    if num_lanes > 2:
        conditions.add(RoadConditionType.MultiLaned)

    print(f"Point: {point.lat}, {point.lng} - Conditions: {conditions}")

    return conditions


# if __name__ == "__main__":
#     print(get_road_conditions(-33.80434765065589, 151.1862909590549))
