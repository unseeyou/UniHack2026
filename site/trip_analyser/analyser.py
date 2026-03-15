from database.trip.trip import Trip
from database.trip.analysis import Analysis
from database.trip.conditions import RoadCondition, WeatherCondition
from trip_analyser.util import reduce_with_distance
from trip_analyser.road_analyser import get_road_conditions
from trip_analyser.trip_weather import get_weather_conditions
from trip_analyser.trip_time import calculate_day_night_time
from database.base import db


def analyse(trip: Trip):
    reduced_points = reduce_with_distance(trip.points, 1)

    road_conditions = get_road_conditions(trip.points)
    weather_conditions = get_weather_conditions(reduced_points)
    day_time, night_time = calculate_day_night_time(reduced_points)

    trip.analysis = Analysis(
        name="Analysed Trip TODO",
        time_day=day_time,
        time_night=night_time,
        road_conditions=set(map(lambda condition: RoadCondition(type=condition), road_conditions)),
        weather_conditions=set(map(lambda condition: WeatherCondition(type=condition), weather_conditions)),
        traffic_conditions=set()
    )

    db.session.commit()
