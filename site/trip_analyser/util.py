from database.trip.trip import Point


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
