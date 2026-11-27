from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from .models import Route, Train, Station, MaintenanceHistory

def home(request):
    return render(request, "core/home.html")

def listRouteView(request):
    data = Route.objects.all()
    context = {"routes" : data}
    return render(request, "core/route_list.html", context)

def listTrainView(request):
    data = Train.objects.all()
    context = {"trains" : data}
    return render(request, "core/train_list.html", context)

class RouteDetailView(TemplateView):
    model = Route
    template_name = "core/route_detail.html"
    context_object_name = "routes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["routes"] = Route.objects.all()
        context["stations"] = Station.objects.all()
        return context



class TrainDetailView(TemplateView):
    model = Train
    template_name = "core/train_detail.html"
    context_object_name = "trains"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["trains"] = Train.objects.all()
            context["records"] = MaintenanceHistory.objects.all()
            return context


