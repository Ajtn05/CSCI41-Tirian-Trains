from django.contrib import admin

from .models import (
    ASeries,
    CrewInCharge,
    InterTownRoute,
    LocalRoute,
    MaintenanceHistory,
    Passenger,
    Route,
    SSeries,
    Station,
    Train,
    TravelDetails,
    TripSchedule,
)


admin.site.register([
    ASeries,
    CrewInCharge,
    InterTownRoute,
    LocalRoute,
    MaintenanceHistory,
    Passenger,
    Route,
    SSeries,
    Station,
    Train,
    TravelDetails,
    TripSchedule,
])
