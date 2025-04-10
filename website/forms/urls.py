from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    # URL for creating a new request
    path('request/', views.create_request, name='create_request'),
    
    # URL for listing all requests
    path('list-requests/', views.list_request, name='list_request'),
    
    # URLs for approving and rejecting requests
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    
    # URL for supervisor review
    path('supervisor-review/<int:request_id>/', views.supervisor_review, name='supervisor_review'),
    
    # URL for assigning engineers (general)
    path('assign-engineer/<int:request_id>/', views.assign_engineer, name='assign_engineer'),
    
    # URL for supervisor assigning engineers
    path('supervisor-assign/<int:request_id>/', views.supervisor_assign_engineer, name='supervisor_assign_engineer'),
]
