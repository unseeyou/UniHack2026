from database.trip.trip import Trip
from database.trip.analysis import Analysis
from trip_analyser.road_analyser import get_road_conditions


def analyse(trip: Trip) -> Analysis:
    road_conditions = set()
    for point in trip.points:
        road_conditions = road_conditions.union(get_road_conditions(point.lat, point.lng))
    