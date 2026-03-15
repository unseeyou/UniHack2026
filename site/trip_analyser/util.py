from database.trip.trip import Point
from datetime import datetime
from zoneinfo import ZoneInfo


def reduce_with_distance(points: list[Point], dist: float) -> list[Point]:
    """dist is in kilometres"""
    if len(points) == 0:
        return []

    spaced_out_points: list[Point] = [points[0]]

    for point in points[1:-1]:
        if point.dist(spaced_out_points[-1]) > dist:
            spaced_out_points.append(point)

    spaced_out_points.append(points[-1])

    return spaced_out_points

def fix_time_zone(points: list[Point]) -> list[Point]:
    new_points = points
    sydney_tz = ZoneInfo("Australia/Sydney")
    utc_tz = ZoneInfo("UTC")

    for point in points:
        if point.time.tzinfo is None:
            point.time = point.time.replace(tzinfo=utc_tz)
        point.time = point.time.astimezone(sydney_tz)
    
    return points

    
