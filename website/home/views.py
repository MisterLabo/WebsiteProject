from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def home_display(request):
    return render(request, 'home.html')
