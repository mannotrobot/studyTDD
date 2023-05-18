from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    """home page my app"""
    return HttpResponse('<html><title><h1>To-Do lists</h1></title></html>')
