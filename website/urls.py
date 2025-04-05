from django.urls import path
from .forms import views

urlpatterns = [
    path('forms/employee-section/', views.employee_section_view, name='employee_section'),
    path('forms/section-manager-section/', views.section_manager_section_view, name='section_manager_section'),
]