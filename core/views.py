from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from .models import Route, Train, Station, MaintenanceHistory, TripSchedule, Ticket, RouteType, LocalRoute, InterTownRoute, TripItinerary

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

def listScheduleView(request):
    data = TripSchedule.objects.all()
    context = {"schedules" : data}
    return render(request, "core/schedule_list.html", context)

def listTicketView(request):
    data = Ticket.objects.all()
    context = {"tickets" : data}
    return render(request, "core/ticket_list.html", context)

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

class ScheduleDetailView(DetailView):
    model = TripSchedule
    template_name = "core/schedule_detail.html"
    context_object_name = "schedule"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route = self.object.route
        if route.type == RouteType.LOCAL:
            context['route'] = LocalRoute.objects.filter(route=route).first()
        else:
            context['route'] = InterTownRoute.objects.filter(route=route).first()
        return context
    

class TicketDetailView(DetailView):
    model = Ticket
    template_name = "core/ticket_detail.html"
    context_object_name = "ticket"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["passenger"] = self.object.passenger
            context["trip_itenerary"] = TripItinerary.objects.filter(ticket=self.object)
            context["schedules"] = []
            for i in context["trip_itenerary"]:
                context["schedules"].append(TripSchedule.objects.filter(id=i.trip_schedule.id).first)
            context["records"] = MaintenanceHistory.objects.all()
            return context



