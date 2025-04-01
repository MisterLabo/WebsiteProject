from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def dashboard_display(request):
    return render(request, 'dashboard.html')