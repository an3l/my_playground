from django.shortcuts import render
from .models import Flight
# Create your views here.

def index(request):
    template_name="_flights_app/index.html"
    context={
        "flights":Flight.objects.all()
    } #context dictionary passes keys and values
    return render(request, template_name, context)
