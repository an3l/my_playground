from django.shortcuts import render
from .models import Flight, Passenger
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def index(request):
    template_name="_flights_app/index.html"
    context={
        "flights":Flight.objects.all(),
    } #context dictionary passes keys and values
    return render(request, template_name, context)

def flight(request, flight_id):
    try:
        flight=Flight.objects.get(pk=flight_id)

    except Flight.DoesNotExist:
        raise Http404("Flight doesn't exist!")
    context={
        "flight":flight,
        "passengers":flight.passengers.all(),
        "non_passengers":Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "_flights_app/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"]) #this will be obtained from flight.html select
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError: # if there is post request without passenger data or a get request
        return render(request, "_flights_app/error.html", {'message': "No selection"})             # there is no passenger data to extract

    except Flight.DoesNotExist:
        context={
            'message':"Flight doesn't exist"
        }
        return render(request, "_flights_app/error.html", context)

    except Passenger.DoesNotExist:
        context={
            'message':"Passenger doesn't exist"
        }
        return render(request, "_flights_app/error.html", context)
    # Add passenger to the flight
    passenger.flights.add(flight)
    # flight is a name of url in urls.py
    return HttpResponseRedirect(reverse("flight", args=(flight_id,) ))
