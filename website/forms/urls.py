from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    path('forms/', views.form_display, name='request'),

]