from django.http import HttpRequest
from scenic.models import *

r = HttpRequest()
r.GET = {'deviceid':'asdfasdfasdfasd', 'device_id':'asdfasd', 'lat':'32','lng':'33','title':'tei', 'trueheading':'23', 'magheading': '42'}

def testContent():
    return ScenicContent.getor(r)

def testUser():
    u = User.getor(r)
    g = GeoPt.getor(r)
    th = getVal(r, 'trueheading')
    mh = getVal(r, 'magheading')
    return UserPicture(user=u, geopt = g, title = 'asdfasdfasdfa', trueHeading =th, magHeading = mh )
    
def aTest():
    return UserContent.getor(r)
