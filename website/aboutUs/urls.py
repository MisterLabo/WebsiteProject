from django.urls import path
from . import views

app_name = 'aboutUs'

urlpatterns = [
    path('aboutUs/', views.about_us_display, name='about_us'),
]