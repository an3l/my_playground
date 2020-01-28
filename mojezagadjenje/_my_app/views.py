from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from scrap_data import *

# Create your views here.
def index(request):
    #return HttpResponse("Hi There")
    template_name="index.html"
    context={
    } #context dictionary passes keys and values
    #x=scrap_data()
    #return HttpResponse(x["Zenica"][0]["url"])

    return render(request, template_name, context)

