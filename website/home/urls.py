from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_display, name="home"),
]
