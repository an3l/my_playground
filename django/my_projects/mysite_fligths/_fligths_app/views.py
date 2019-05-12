from django.shortcuts import render
from .models import Flight
from django.http import HttpResponse, Http404
# Create your views here.

def index(request):
    template_name="_flights_app/index.html"
    context={
        "flights":Flight.objects.all()
    } #context dictionary passes keys and values
    return render(request, template_name, context)

def flight(request, flight_id):
    try:
        flight=Flight.objects.get(pk=flight_id)

    except Flight.DoesNotExist:
        raise Http404("Flight doesn't exist!")
    context={
        "flight":flight
    }
    return render(request, "_flights_app/flight.html", context)
