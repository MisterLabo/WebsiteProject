from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def form_display(request):
    return render(request, 'form.html')