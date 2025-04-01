from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def personal_profile_display(request):
    return render(request, 'personalProfile.html')