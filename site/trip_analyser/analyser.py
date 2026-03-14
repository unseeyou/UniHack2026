from database.trip.trip import Trip
from database.trip.analysis import Analysis
from database.trip.conditions import RoadCondition
from trip_analyser.road_analyser import get_road_conditions
from celery_app import celery_app
from database.base import db

@celery_app.task()
def analyse(trip: Trip):
    road_conditions = set()
    for point in trip.points:
        road_conditions = road_conditions.union(get_road_conditions(point.lat, point.lng))

    # TODO

    trip.analysis = Analysis(
        road_conditions=set(map(lambda condition: RoadCondition(type=condition), road_conditions))
    )

    db.session.commit()
