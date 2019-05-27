from django.urls import path

from django.urls import path
from . import views
# we could say: from application import views as application_view and use it as application_view.details

app_name = 'tehnicka'
urlpatterns = [
    path("", views.index, name='index'),
    path("details/<int:ucenik_id>", views.details, name='details'),
    path("delete/<int:ucenik_id>", views.delete, name='delete'),
    path("add-student/", views.dodajucenika, name='dodajucenika'),
    path("details/priznanje/<int:priznanje_id>", views.brisipriznanje, name='brisipriznanje'),
]
