from django.db import models

# Create your models here.
class GeoPt(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()

class Route(models.Model):
    plString = models.CharField(max_length=1000)

class Device(models.Model):
    device = models.CharField(max_length=40, unique=True)

class Rating(models.Model):
    device = models.ForeignKey(Device)
    route  = models.ForeignKey(Route, related_name="%(app_label)s_%(class)s_related")
    rating = models.IntegerField()
    class Meta:
        unique_together = ("device", "route")
