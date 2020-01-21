from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index(request):
    #return HttpResponse("Hi There")
    template_name="_flights_app/index.html"
    context={
        "flights":Flight.objects.all(),
    } #context dictionary passes keys and values
    return render(request, template_name, context)

def index1(request, index1):
    return HttpResponse('Hi '+str(index1))
