from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    path('forms/', views.form_display, name='request'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('manager-approval/', views.manager_approval, name='approval'),
    path('receiver-action/', views.receiver_action, name='designer'),
    path('validation-action/', views.validation_action, name='validation'),
]