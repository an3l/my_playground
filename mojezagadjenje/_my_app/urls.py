from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:index1>", views.index1, name="index1"),
    #path("<int:flight_id>/book", views.book, name="book"),
]
