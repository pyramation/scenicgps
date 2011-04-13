import sys, os
import django.core.handlers.wsgi
cwd = os.getcwd()
myapp_directory = cwd + '/scenicgps'
sys.path.insert(0,myapp_directory)
sys.path.append(cwd)
os.environ['DJANGO_SETTINGS_MODULE'] = "scenicgps.settings"
application = django.core.handlers.wsgi.WSGIHandler()
