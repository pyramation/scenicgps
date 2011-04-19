from django.http import HttpResponse
from django.utils.simplejson import dumps


SUC_VAL = 'ok'
ERR_VAL = 'error'
STATUS_KEY = 'status'

def jsonRes(dic):
	return HttpResponse(dumps(dic))

def success():
	return jsonRes({STATUS_KEY: SUC_VAL})
def error():
	return jsonRes({STATUS_KEY: ERR_VAL})
def postMethod(f):
	def new_f(request):
		try:
			f(request)
			return success()
		except:
			return error()
	return new_f
	
