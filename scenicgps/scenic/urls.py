from django.conf.urls.defaults import *

urlpatterns = patterns('scenic.views',
    (r'^$', 'index'),
)