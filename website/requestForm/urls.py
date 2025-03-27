from django.urls import path
from . import views

urlpatterns = [
    path("", views.requestForm_request, name="Machine Engineering Request Form"),
]
