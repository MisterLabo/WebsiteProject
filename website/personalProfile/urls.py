from django.urls import path
from . import views

app_name = 'personalProfile'

urlpatterns = [
    path('profile/', views.personal_profile_display, name='Profile'),
]