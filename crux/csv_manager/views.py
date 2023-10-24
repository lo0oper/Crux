from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(req):
    return HttpResponse("HOME",req)

def room(req):
    return HttpResponse("Room",req)