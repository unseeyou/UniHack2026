import requests

from constants import app
from database.trip.trip import Point
from database.trip.conditions import RoadConditionType

from shapely.geometry import Point as ShapelyPoint, LineString
from shapely.strtree import STRtree


def parse_lanes(lanes_str: str) -> int:
    """Safely parse messy OSM lane strings like '1-2', 'yes', or '2;3'."""
    try:
        return int(str(lanes_str).split(";")[0].split("-")[0])
    except ValueError, TypeError:
        return 1


def get_road_conditions(points: list[Point]) -> set[RoadConditionType]:  # shoutout to gemini for the assist
    """
    Analyzes a list of trip points in a single bulk Overpass query,
    matches them locally using Shapely, and returns all unique road conditions encountered.
    """
    if not points:
        return set()

    # 1. Calculate bounding box for the entire trip with a small buffer (~50m / 0.0005 deg)
    buffer = 0.0005
    lats = [p.lat for p in points]
    lngs = [p.lng for p in points]
    min_lat, max_lat = min(lats) - buffer, max(lats) + buffer
    min_lng, max_lng = min(lngs) - buffer, max(lngs) + buffer

    # 2. Single Overpass query using 'out geom;' to fetch ways and their coordinate arrays directly
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    way["highway"]({min_lat},{min_lng},{max_lat},{max_lng});
    out geom;
    """

    user_agent = "RoadAnalyser/0.2 (+https://test.unseeyou.com; contact@unseeyou.com)"

    try:
        response = requests.post(
            overpass_url, data={"data": query}, headers={"User-Agent": user_agent}
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        app.logger.error(f"Overpass API request failed: {e}")
        return set()

    if "<html>" in response.text:
        app.logger.error("Received HTML error page from Overpass.")
        return set()

    # 3. Build local Shapely geometries and a spatial index (STRtree) for fast querying
    linestrings = []
    way_data_list = []

    for element in data.get("elements", []):
        if element.get("type") == "way" and "geometry" in element:
            coords = [(node["lon"], node["lat"]) for node in element["geometry"]]
            if len(coords) >= 2:
                line = LineString(coords)
                linestrings.append(line)
                way_data_list.append({"tags": element.get("tags", {}), "line": line})

    if not linestrings:
        app.logger.error("No valid road geometries found in bounding box.")
        return set()

    # STRtree allows lightning-fast spatial nearest-neighbor searches locally
    tree = STRtree(linestrings)

    # Define surface and highway classifications
    unsealed_surfaces = {
        "unpaved",
        "gravel",
        "dirt",
        "sand",
        "earth",
        "ground",
        "compacted",
    }
    sealed_surfaces = {"asphalt", "paved", "concrete", "bitumen", "paving_stones"}
    main_road_highway_types = {
        "primary",
        "secondary",
        "primary_link",
        "secondary_link",
        "motorway",
        "trunk",
        "motorway_link",
    }
    quiet_street_highway_types = {
        "residential",
        "living_street",
        "tertiary",
        "tertiary_link",
    }

    trip_conditions = set()

    # 4. Process each trip point locally
    for pt in points:
        shapely_pt = ShapelyPoint(
            pt.lng, pt.lat
        )  # Shapely uses (longitude, latitude) order

        # Query the spatial index for the nearest road geometry index
        nearest_idx = tree.nearest(shapely_pt)
        matched_way = way_data_list[nearest_idx]
        tags = matched_way["tags"]

        highway_type = tags.get("highway", "").casefold()
        surface = tags.get("surface", "").casefold()
        num_lanes = parse_lanes(tags.get("lanes", 1))

        # Evaluate conditions
        if surface in unsealed_surfaces:
            trip_conditions.add(RoadConditionType.Unsealed)
        if surface in sealed_surfaces:
            trip_conditions.add(RoadConditionType.Sealed)
        if highway_type in main_road_highway_types:
            trip_conditions.add(RoadConditionType.MainRoad)
        if highway_type in quiet_street_highway_types:
            trip_conditions.add(RoadConditionType.QuietStreet)
        if num_lanes > 2:
            trip_conditions.add(RoadConditionType.MultiLaned)

    return trip_conditions
