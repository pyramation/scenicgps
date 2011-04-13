# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from scenicgps.scenic.models import *
from django.utils.simplejson import dumps


def index(request):
    return HttpResponse('hello world')

def putRoute(request):
    plString = request.GET['plstring']
    rating = int(request.GET['rating'])
    try:
        Route(plString = plString, rating = rating).save()
        return HttpResponse(dumps({'status':'ok'}))
    except:
        return HttpResponse(dumps({'status':'error'}))


