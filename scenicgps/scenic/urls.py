from django.conf.urls.defaults import *

urlpatterns = patterns('scenic.views',
    (r'^putroute$','putRoute'),
    (r'^panrate$','ratePanoramio'),
    (r'^getuserphotos$','userPhotos'),
    (r'^getallphotos$','allUserPhotos'),
    (r'^lastroute$','lastRoute'),
    (r'^uploadphoto$', 'uploadPhoto'),
    (r'^$', 'index'),                     
)
