from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    path('request/', views.create_request, name='create_request'),
    path('requestlist/', views.list_request, name='list_request'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('supervisor-review/<int:request_id>/', views.supervisor_review, name='supervisor_review'),
    path('assign-engineer/<int:request_id>/', views.assign_engineer, name='assign_engineer'),
]
