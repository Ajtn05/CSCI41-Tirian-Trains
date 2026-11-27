from django.db import models
from django.db.models import F, Q

from .validators import (
    A_MODEL_PATTERN,
    INITIAL_PATTERN,
    S_MODEL_PATTERN,
    a_model_validator,
    initial_validator,
    s_model_validator,
    validate_not_future,
)

CURRENT_DATE = models.Func(
    function="CURRENT_DATE",
    template="%(function)s",
    output_field=models.DateField(),
)


class Gender(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    OTHER = "Other", "Other"
    PRIVATE = "Prefer Not to Say", "Prefer Not to Say"


class RouteType(models.TextChoices):
    LOCAL = "local", "Local"
    INTER_TOWN = "inter-town", "Inter-town"


class TrainType(models.TextChoices):
    A_SERIES = "A", "A series"
    S_SERIES = "S", "S series"


class Condition(models.TextChoices):
    EXCELLENT = "Excellent", "Excellent"
    VERY_GOOD = "Very Good", "Very Good"
    GOOD = "Good", "Good"
    SATISFACTORY = "Satisfactory", "Satisfactory"
    FAIR = "Fair", "Fair"
    POOR = "Poor", "Poor"
    VERY_POOR = "Very Poor", "Very Poor"


# 1. PASSENGER
class Passenger(models.Model):
    id = models.IntegerField(primary_key=True, db_column="passenger_id")
    last_name = models.CharField(max_length=50)
    given_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=2, validators=[initial_validator])
    birth_date = models.DateField(validators=[validate_not_future])
    gender = models.CharField(max_length=50, choices=Gender.choices)

    class Meta:
        db_table = "passenger"
        constraints = [
            models.CheckConstraint(condition=Q(id__gt=0), name="passenger_positive_id"),
            models.CheckConstraint(
                condition=Q(middle_initial__regex=INITIAL_PATTERN),
                name="passenger_initial_format",
            ),
            models.CheckConstraint(condition=Q(birth_date__lte=CURRENT_DATE), name="passenger_birth_date"),
            models.CheckConstraint(condition=Q(gender__in=Gender.values), name="passenger_valid_gender"),
        ]

    def __str__(self):
        return f"{self.given_name} {self.middle_initial} {self.last_name}"


# 2. STATION
class Station(models.Model):
    id = models.IntegerField(primary_key=True, db_column="station_id")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "station"
        constraints = [
            models.CheckConstraint(condition=Q(id__gt=0), name="station_positive_id"),
        ]

    def __str__(self):
        return self.name


# 3. ROUTE
# Discuss where to store the shared local fare so it can change over time.
class Route(models.Model):
    id = models.IntegerField(primary_key=True, db_column="route_id")
    travel_time = models.IntegerField(verbose_name="travel time in minutes")
    cost = models.IntegerField(verbose_name="fare in Lion coins")
    type = models.CharField(max_length=20, choices=RouteType.choices)

    class Meta:
        db_table = "route"
        constraints = [
            models.CheckConstraint(condition=Q(id__gt=0), name="route_positive_id"),
            models.CheckConstraint(condition=Q(travel_time__gt=0), name="route_positive_travel_time"),
            models.CheckConstraint(condition=Q(cost__gt=0), name="route_positive_cost"),
            models.CheckConstraint(condition=Q(type__in=RouteType.values), name="route_valid_type"),
        ]

    def __str__(self):
        return f"{self.get_type_display()} route {self.pk}"


# 4. TRAIN
class Train(models.Model):
    id = models.IntegerField(primary_key=True, db_column="train_id")
    max_speed = models.IntegerField()
    number_of_seats = models.PositiveIntegerField()
    number_of_toilets = models.PositiveIntegerField(default=0, db_default=0)
    reclining_seats = models.BooleanField(default=False, db_default=False)
    folding_tables = models.BooleanField(default=False, db_default=False)
    disability_access = models.BooleanField(default=False, db_default=False)
    luggage_storage = models.BooleanField(default=False, db_default=False)
    vending_machines = models.BooleanField(default=False, db_default=False)
    food_service = models.BooleanField(default=False, db_default=False)
    type = models.CharField(max_length=1, choices=TrainType.choices)

    class Meta:
        db_table = "train"
        constraints = [
            models.CheckConstraint(condition=Q(id__gt=0), name="train_positive_id"),
            models.CheckConstraint(condition=Q(max_speed__gt=0), name="train_positive_max_speed"),
            models.CheckConstraint(condition=Q(type__in=TrainType.values), name="train_valid_type"),
        ]

    def __str__(self):
        return f"{self.get_type_display()} train {self.pk}"


# 5. CREW_IN_CHARGE
class CrewInCharge(models.Model):
    id = models.IntegerField(primary_key=True, db_column="crew_id")
    first_name_initial = models.CharField(max_length=2, validators=[initial_validator])
    last_name = models.CharField(max_length=50)

    class Meta:
        db_table = "crew_in_charge"
        verbose_name_plural = "crew members"
        constraints = [
            models.CheckConstraint(condition=Q(id__gt=0), name="crew_positive_id"),
            models.CheckConstraint(
                condition=Q(first_name_initial__regex=INITIAL_PATTERN),
                name="crew_initial_format",
            ),
        ]

    def __str__(self):
        return f"{self.first_name_initial} {self.last_name}"


# 6. LOCAL_ROUTE
class LocalRoute(models.Model):
    route = models.OneToOneField(
        Route,
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="local_route",
        db_column="local_route_id",
    )
    start_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="local_routes_starting_here",
    )
    end_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="local_routes_ending_here",
    )

    class Meta:
        db_table = "local_route"
        constraints = [
            models.CheckConstraint(
                condition=~Q(start_station=F("end_station")),
                name="local_route_distinct_stations",
            ),
        ]

    def __str__(self):
        return f"{self.start_station} to {self.end_station}"


# 7. INTER_TOWN_ROUTE
class InterTownRoute(models.Model):
    route = models.OneToOneField(
        Route,
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="inter_town_route",
        db_column="inter_town_route_id",
    )

    class Meta:
        db_table = "inter_town_route"

    def __str__(self):
        return str(self.route)


# 8. TRAVEL_DETAILS
class TravelDetails(models.Model):
    route = models.OneToOneField(
        Route,
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="travel_details",
    )
    origin = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="routes_from",
        db_column="origin",
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="routes_to",
        db_column="destination",
    )

    class Meta:
        db_table = "travel_details"
        verbose_name_plural = "travel details"
        constraints = [
            models.CheckConstraint(
                condition=~Q(origin=F("destination")),
                name="travel_details_distinct_stations",
            ),
        ]

    def __str__(self):
        return f"{self.origin} to {self.destination}"


# 9. TICKET
class Ticket(models.Model):
    id = models.IntegerField(primary_key=True, db_column="ticket_id")
    purchase_date = models.DateField(validators=[validate_not_future])
    total_cost = models.PositiveIntegerField(default=0, db_default=0)
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    class Meta:
        db_table = "ticket"
        constraints = [
            models.CheckConstraint(condition=Q(id__gt=0), name="ticket_positive_id"),
            models.CheckConstraint(condition=Q(purchase_date__lte=CURRENT_DATE), name="ticket_purchase_date"),
        ]

    def __str__(self):
        return f"Ticket {self.pk}"


# 10. MAINTENANCE_HISTORY
class MaintenanceHistory(models.Model):
    id = models.IntegerField(primary_key=True, db_column="maintenance_id")
    train = models.ForeignKey(
        Train,
        on_delete=models.PROTECT,
        related_name="maintenance_records",
    )
    crew = models.ForeignKey(
        CrewInCharge,
        on_delete=models.PROTECT,
        related_name="maintenance_records",
    )
    date = models.DateField(validators=[validate_not_future])
    tasks = models.CharField(max_length=255)
    condition = models.CharField(max_length=255, choices=Condition.choices)

    class Meta:
        db_table = "maintenance_history"
        verbose_name_plural = "maintenance history"
        constraints = [
            models.CheckConstraint(
                condition=Q(condition__in=Condition.values),
                name="maintenance_valid_condition",
            ),
            models.CheckConstraint(condition=Q(date__lte=CURRENT_DATE), name="maintenance_date"),
        ]

    def __str__(self):
        return f"{self.train} on {self.date}"


# 11. INTER_TOWN_ROUTE_STATION
class InterTownRouteStation(models.Model):
    pk = models.CompositePrimaryKey(
        "inter_town_route_id",
        "station_slot",
    )
    inter_town_route = models.ForeignKey(
        InterTownRoute,
        on_delete=models.PROTECT,
        related_name="station_links",
    )
    station_slot = models.IntegerField()
    station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="inter_town_route_links",
    )

    class Meta:
        db_table = "inter_town_route_station"
        constraints = [
            models.CheckConstraint(
                condition=Q(station_slot__in=(0, 1)),
                name="inter_town_valid_station_slot",
            ),
            models.UniqueConstraint(
                fields=("inter_town_route", "station"),
                name="inter_town_distinct_stations",
            ),
        ]

    def __str__(self):
        return f"Route {self.inter_town_route_id}, slot {self.station_slot}: {self.station}"


# 12. TRIP_SCHEDULE
class TripSchedule(models.Model):
    id = models.IntegerField(primary_key=True, db_column="trip_schedule_id")
    date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    route = models.ForeignKey(
        Route,
        on_delete=models.PROTECT,
        related_name="schedules",
    )
    train = models.ForeignKey(
        Train,
        on_delete=models.PROTECT,
        related_name="schedules",
    )

    class Meta:
        db_table = "trip_schedule"
        constraints = [
            models.CheckConstraint(condition=Q(id__gt=0), name="schedule_positive_id"),
        ]

    def __str__(self):
        return f"{self.route} on {self.date} at {self.departure_time}"


# 13. A_SERIES
class ASeries(models.Model):
    train = models.OneToOneField(
        Train,
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="a_series",
        db_column="a_train_id",
    )
    model = models.CharField(max_length=50, validators=[a_model_validator])
    assigned_route = models.ForeignKey(
        InterTownRoute,
        on_delete=models.PROTECT,
        related_name="assigned_trains",
        db_column="a_route_id",
    )

    class Meta:
        db_table = "a_series"
        verbose_name_plural = "A-series trains"
        constraints = [
            models.CheckConstraint(condition=Q(model__regex=A_MODEL_PATTERN), name="a_series_model_format"),
        ]

    def __str__(self):
        return self.model


# 14. S_SERIES
class SSeries(models.Model):
    train = models.OneToOneField(
        Train,
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="s_series",
        db_column="s_train_id",
    )
    model = models.CharField(max_length=50, validators=[s_model_validator])
    assigned_route = models.ForeignKey(
        LocalRoute,
        on_delete=models.PROTECT,
        related_name="assigned_trains",
        db_column="s_route_id",
    )

    class Meta:
        db_table = "s_series"
        verbose_name_plural = "S-series trains"
        constraints = [
            models.CheckConstraint(condition=Q(model__regex=S_MODEL_PATTERN), name="s_series_model_format"),
        ]

    def __str__(self):
        return self.model


# 15. TRIP_ITINERARY
class TripItinerary(models.Model):
    pk = models.CompositePrimaryKey(
        "ticket_id",
        "trip_schedule_id",
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.PROTECT,
        related_name="itinerary",
    )
    trip_schedule = models.ForeignKey(
        TripSchedule,
        on_delete=models.PROTECT,
        related_name="itinerary",
    )
    historical_cost = models.PositiveIntegerField(default=0, db_default=0)

    class Meta:
        db_table = "trip_itinerary"
        verbose_name_plural = "trip itineraries"

    def __str__(self):
        return f"Ticket {self.ticket_id}, trip {self.trip_schedule_id}"
