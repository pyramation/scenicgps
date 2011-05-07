from django.http import HttpRequest
from scenic.models import *


def testContent():
    r = HttpRequest()
    r.GET = {'device_id':'asdfasd', 'lat':'32','lng':'33','title':'tei'}
    return ScenicContent.getor(r)

def testUser():
    r = HttpRequest()
    r.GET = {'deviceid':'asdfasdfasdfasd', 'device_id':'asdfasd', 'lat':'32','lng':'33','title':'tei', 'trueheading':'23', 'magheading': '42'}
    u = User.getor(r)
    g = GeoPt.getor(r)
    th = getVal(r, 'trueheading')
    mh = getVal(r, 'magheading')
    return UserPicture(user=u, geopt = g, title = 'asdfasdfasdfa', trueHeading =th, magHeading = mh )
    
def aTest():
    r = HttpRequest()
    r.GET = {'deviceid':'asdfasdfaasd', 'lat':'12','lng':'33','title':'tei', 'trueheading':'23', 'magheading': '42'}
    return UserContent.getor(r)
