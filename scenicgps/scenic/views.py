# Create your views here.
from scenicgps.scenic.models import *
from scenicgps.utils import *




@postMethod
def index(request):
	pass

@postMethod
def putRoute(request):
	Route.rateRoute(request)

@postMethod
def ratePanoramio(request):
	ScenicContent.setRating(PanoramioContent.getor(request), request)

