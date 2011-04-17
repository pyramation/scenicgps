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
    device = request.GET['device']
    try:

	    try:
            rte = Route.objects.get(plString = plString)
	    except:
            rte = Route(plString = plString)
	        rte.save()

	    try:
            dev=Device.objects.get(device=device)
        except:
            dev=Device(device=device)
            dev.save()

        try:
	        rate = Rating.objects.get(route = rte, device = dev)
            rate.rating = rating
            rate.save()
        except:
            Rating(route = rte, device = dev, rating = rating).save()


        return HttpResponse(dumps({'status':'ok'}))
    except:
        return HttpResponse(dumps({'status':'error'}))


