# Create your views here.
from scenicgps.scenic.models import *
from scenicgps.utils import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@postMethod
def index(request):
	pass



@csrf_exempt
@postMethod
def uploadPhoto(request):
	if request.method == 'POST':
		UserPicture.putPhoto(request)
		

@postMethod
def putRoute(request):
	Route.rateRoute(request)

@postMethod
def ratePanoramio(request):
	ScenicContent.setRating(PanoramioContent.getor(request), request)

@getMethod
def lastRoute(request):
	return {Route.PLKEY : Route.lastRoute().plString}

@getMethod
def userPhotos(request):
	return {UserPicture.SET_KEY : UserPicture.fetchPictures(request)}

@getMethod
def allUserPhotos(request):
	return {UserPicture.SET_KEY : UserPicture.fetchAllPictures(request)}

@getMethod
def nearby(request):
	return {UserPicture.SET_KEY : [x.toDic() for x in UserPicture.nearby(request)]}
