from django.http import HttpResponse
from django.utils.simplejson import dumps


SUC_VAL = 'ok'
ERR_VAL = 'error'
STATUS_KEY = 'status'
RESPONSE_KEY = 'response'
SC_DIC = {STATUS_KEY: SUC_VAL}
ERR_DIC = {STATUS_KEY: ERR_VAL}



def jsonRes(dic):
	return HttpResponse(dumps(dic))

def success():
	return jsonRes(SC_DIC)
def error():
	return jsonRes(ERR_DIC)



def postMethod(f):
	def new_f(request):
		try:
			f(request)
			return success()
		except:
			return error()
	return new_f
	
def getMethod(f):
	def new_f(request):
		try:
			return getResponse(f(request))
		except:
			return error()
	return new_f

def getResponse(response):
	res = {RESPONSE_KEY:response}
	res[STATUS_KEY] = SUC_VAL
	return jsonRes(res)
