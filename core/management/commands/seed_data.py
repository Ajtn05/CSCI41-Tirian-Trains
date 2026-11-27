from datetime import date, time, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import (
    ASeries,
    Condition,
    CrewInCharge,
    Gender,
    InterTownRoute,
    InterTownRouteStation,
    LocalRoute,
    MaintenanceHistory,
    Passenger,
    Route,
    RouteType,
    SSeries,
    Station,
    Ticket,
    Train,
    TrainType,
    TravelDetails,
    TripItinerary,
    TripSchedule,
)


class Command(BaseCommand):
    help = "Load sample routes, trains, and a two-trip ticket into a development database."

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.localdate()
        service_date = today + timedelta(days=1)
        new_records = 0

        # Fixed IDs let later tables reference the sample rows directly.
        def seed(model, *, defaults=None, **lookup):
            nonlocal new_records
            _, created = model.objects.get_or_create(defaults=defaults, **lookup)
            new_records += created

        # Stations and crew
        stations = [
            (9001, "Beaver's Dam"),
            (9002, "Allies' Enclave"),
            (9003, "Cauldron Pool"),
            (9004, "Cherry Tree"),
        ]
        for station_id, name in stations:
            seed(Station, pk=station_id, name=name)

        seed(CrewInCharge, pk=9001, first_name_initial="B.", last_name="Ramoh")

        # Routes and their endpoints
        routes = [
            (9001, RouteType.LOCAL, 5, 2),
            (9002, RouteType.INTER_TOWN, 127, 6),
            (9003, RouteType.INTER_TOWN, 390, 20),
        ]
        for route_id, route_type, minutes, fare in routes:
            seed(Route, pk=route_id, type=route_type, defaults={"travel_time": minutes, "cost": fare})

        seed(LocalRoute, route_id=9001, start_station_id=9001, end_station_id=9002)
        for route_id in (9002, 9003):
            seed(InterTownRoute, route_id=route_id)

        inter_town_stations = [
            (9002, 0, 9002),
            (9002, 1, 9003),
            (9003, 0, 9003),
            (9003, 1, 9004),
        ]
        for route_id, slot, station_id in inter_town_stations:
            seed(InterTownRouteStation, inter_town_route_id=route_id, station_slot=slot, station_id=station_id)

        travel_details = [(9001, 9001, 9002), (9002, 9002, 9003), (9003, 9003, 9004)]
        for route_id, origin_id, destination_id in travel_details:
            seed(TravelDetails, route_id=route_id, origin_id=origin_id, destination_id=destination_id)

        # Trains and maintenance
        trains = [(9001, TrainType.S_SERIES), (9002, TrainType.A_SERIES), (9003, TrainType.A_SERIES)]
        for train_id, train_type in trains:
            seed(Train, pk=train_id, type=train_type, defaults={"max_speed": 120, "number_of_seats": 70})

        seed(SSeries, train_id=9001, assigned_route_id=9001, defaults={"model": "S-393"})
        seed(ASeries, train_id=9002, assigned_route_id=9002, defaults={"model": "A-9002"})
        seed(ASeries, train_id=9003, assigned_route_id=9003, defaults={"model": "A-9003"})

        for train_id, _ in trains:
            seed(
                MaintenanceHistory,
                pk=train_id,
                train_id=train_id,
                defaults={"crew_id": 9001, "date": today, "tasks": "Cleaning", "condition": Condition.EXCELLENT},
            )

        # Scheduled trips
        schedules = [
            (9001, 9001, 9001, time(8, 15), time(8, 20)),
            (9002, 9002, 9002, time(9, 41), time(11, 48)),
            (9003, 9003, 9003, time(12), time(18, 30)),
        ]
        for schedule_id, route_id, train_id, departure, arrival in schedules:
            seed(
                TripSchedule,
                pk=schedule_id,
                route_id=route_id,
                train_id=train_id,
                defaults={"date": service_date, "departure_time": departure, "arrival_time": arrival},
            )

        # Passenger, ticket, and itinerary
        seed(
            Passenger,
            pk=9001,
            given_name="Adam",
            last_name="Grove",
            defaults={"middle_initial": "K.", "birth_date": date(1972, 6, 1), "gender": Gender.MALE},
        )
        seed(Ticket, pk=9001, passenger_id=9001, defaults={"purchase_date": today, "total_cost": 26})
        for schedule_id, fare in [(9002, 6), (9003, 20)]:
            seed(TripItinerary, ticket_id=9001, trip_schedule_id=schedule_id, defaults={"historical_cost": fare})

        self.stdout.write(f"Added {new_records} demo records. Ticket 9001 covers two inter-town trips.")
