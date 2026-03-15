from database.trip.trip import Trip
from database.trip.analysis import Analysis
from database.trip.conditions import RoadCondition, WeatherCondition, TrafficCondition
from trip_analyser.util import reduce_with_distance, fix_time_zone
from trip_analyser.road_analyser import get_road_conditions
from trip_analyser.trip_weather import get_weather_conditions
from trip_analyser.trip_time import calculate_day_night_time
from trip_analyser.trip_traffic import trip_traffic_analysis
from trip_analyser.trip_suburbs import get_start_end_locations
from database.base import db


def analyse(trip: Trip):
    print(f"Analysing trip with id: {trip.id}")
    reduced_points = reduce_with_distance(trip.points, 1)
    print(f"Reduced points from {len(trip.points)} to {len(reduced_points)}")

    road_conditions = get_road_conditions(trip.points)
    print(f"Road conditions: {road_conditions}")

    weather_conditions = get_weather_conditions(reduced_points)
    weather_conditions_str = ", ".join(weather_conditions)
    print(f"Weather conditions: {weather_conditions_str}")

    day_time, night_time = calculate_day_night_time(fix_time_zone(reduced_points))
    print(f"Day time: {day_time} seconds, Night time: {night_time} seconds")

    traffic_conditions = [trip_traffic_analysis(trip.points)]
    print(f"Traffic conditions: {traffic_conditions}")

    locations = get_start_end_locations(trip.points)
    print(f"Locations: {locations}")


    trip.analysis = Analysis(
        name=locations,
        time_day=day_time,
        time_night=night_time,
        road_conditions=set(map(lambda condition: RoadCondition(type=condition), road_conditions)),
        weather_conditions=set(map(lambda condition: WeatherCondition(type=condition), weather_conditions)),
        traffic_conditions=set(map(lambda condition: TrafficCondition(type=condition), traffic_conditions))
    )

    db.session.commit()
