from django.conf.urls.defaults import *

urlpatterns = patterns('scenic.views',
    (r'^putroute$','putRoute'),
    (r'^panrate$','ratePanoramio'),
    (r'^$', 'index'),
)
