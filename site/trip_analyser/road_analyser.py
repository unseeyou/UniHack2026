import requests
from constants import app
from database.trip.trip import Point
from database.trip.conditions import RoadConditionType


def get_road_conditions(points: list[Point]) -> set[RoadConditionType]:
    road_conditions = set()

    for point in points:
        road_conditions = road_conditions.union(get_point_road_conditions(point))

    return road_conditions


def get_point_road_conditions(point: Point) -> set[RoadConditionType]:
    overpass_url = "https://overpass.thepyes.au/api/interpreter"

    # Query finds the nearest 'way' with a 'highway' tag within 20m
    query = f"""
    [out:json];
    way(around:20, {point.lat}, {point.lng})[highway];
    out tags;
    """

    try:
        response = requests.post(overpass_url, data={"data": query})
        data = response.json()
    except Exception as e:
        app.logger.exception(e)
        print(response.content)
        return []

    # First element is closest element
    tags = data["elements"][0].get("tags", {})

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

    return conditions


# if __name__ == "__main__":
#     print(get_road_conditions(-33.80434765065589, 151.1862909590549))
