from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def requestForm_request(request):
    return HttpResponse("This is the Machine Engineering Request Form")
