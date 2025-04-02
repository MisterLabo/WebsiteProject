from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def about_us_display(request):
    return render(request, 'about.html')