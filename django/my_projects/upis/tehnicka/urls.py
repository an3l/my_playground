from django.urls import path

from django.urls import path
from . import views
# we could say: from application import views as application_view and use it as application_view.details

app_name = 'tehnicka'
urlpatterns = [
    path("", views.index, name='index'),
    path("details/<int:ucenik_id>", views.details, name='details'),
    #path("edit/<int:ucenik_id>", views.editucenika, name='editucenik'),
    path("add-student/", views.dodajucenika, name='dodajucenika')
]
