from django.db import models

# Create your models here.
class GeoPt(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()

class Route(models.Model):
    plString = models.CharField(max_length=1000)
    rating = models.IntegerField()



