from django.urls import path

from . import views
from .views import listRouteView, RouteDetailView, listTrainView, TrainDetailView



app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("route_list", listRouteView, name="routes"),
    path("route_detail", RouteDetailView.as_view(), name="route_detail"),
    path("train_list", listTrainView, name="trains"),
    path("train_detail", TrainDetailView.as_view(), name="train_detail")
]
