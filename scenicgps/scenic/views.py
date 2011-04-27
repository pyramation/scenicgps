# Create your views here.
from scenicgps.scenic.models import *
from scenicgps.utils import *
from django.views.decorators.csrf import csrf_exempt



@postMethod
def index(request):
	pass


@postMethod
@csrf_exempt
def uploadPhoto(request):
	if request.method == 'POST':
		form = PhotoForm

@postMethod
def putRoute(request):
	Route.rateRoute(request)

@postMethod
def ratePanoramio(request):
	ScenicContent.setRating(PanoramioContent.getor(request), request)

@getMethod
def lastRoute(request):
	return {Route.PLKEY : Route.lastRoute().plString}
