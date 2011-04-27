#from django.contrib.gis.db import models
from django.db import models
import os
def getOrCreate(cls, **kwargs):
    return cls.objects.get_or_create(**kwargs)[0]

def getVal(request,key):
    try:
        result = request.GET[key]
        if isinstance(result,str) or isinstance(result,unicode):
            return result
        return result[0]
    except:
        return None

def getRating(request):
    KEY = 'rating'
    return int(getVal(request,KEY))



# Create your models here.
class GeoPt(models.Model):
    LATKEY = 'lat'
    LNGKEY = 'lng'
    lat = models.FloatField()
    lng = models.FloatField()
    
    @classmethod
    def getor(cls,request):
        return getOrCreate(cls,lat=cls.getLat(request),lng=cls.getLng(request))

    @classmethod
    def getLat(cls,request):
        return float(getVal(request,cls.LATKEY))

    @classmethod
    def getLng(cls,request):
        val = getVal(request,cls.LNGKEY)
        return float(val)
    

        
        
        

class Route(models.Model):
    PLKEY = 'plstring'
    date = models.DateTimeField(auto_now=True)

    plString = models.CharField(max_length=3000)
    
    @classmethod
    def getor(cls,request):
        return getOrCreate(cls,plString = cls.getPL(request))

    @classmethod
    def lastRoute(cls):
        return cls.objects.order_by('-date')[0]
        

    @classmethod
    def getPL(cls, request):
        return getVal(request,cls.PLKEY)

    @classmethod
    def rateRoute(cls,request):
        route = cls.getor(request)
        rating = getRating(request)
        user = User.getor(request)
        RouteRating.setRating(route,user,rating)

class User(models.Model):
    DEVKEY = 'deviceid'
    device_id = models.CharField(max_length=40, unique = True)

    @classmethod
    def getor(cls,request):
        return getOrCreate(cls,device_id=getVal(request,cls.DEVKEY))
        

class RouteRating(models.Model):
    user = models.ForeignKey(User)
    route  = models.ForeignKey(Route, related_name="%(app_label)s_%(class)s_related")
    rating = models.IntegerField(default=0)
    class Meta:
        unique_together = ("user", "route")

    @classmethod
    def getor(cls, route, user):
        return getOrCreate(cls,route = route, user = user)

    @classmethod
    def setRating(cls, route, user, rating):
        rtrating = cls.getor(route,user)
        rtrating.rating = rating
        rtrating.save()

class ScenicContent(models.Model):
    TITLEKEY = 'title'
    title = models.CharField(max_length=200)
    geopt = models.ForeignKey(GeoPt, related_name='%(app_label)s_%(class)s_related')

    @classmethod
    def getor(cls,request):
        return getOrCreate(cls,title=getVal(request,TITLEKEY), geopt = GeoPt.getor(request))


    def rate(self, request):
        rating = getRating(request)
        contentRating = ContentRating.getor(request)


    @classmethod
    def getTitle(cls, request):
        return getVal(request,cls.TITLEKEY)

    @classmethod
    def setRating(cls,content, request):
        user = User.getor(request)
        rating = getRating(request)
        content.setMyRating(user,rating)

    
    def setMyRating(self, user, rating):
        ContentRating.setRating(self, user,rating)


    

class PanoramioContent(ScenicContent):
    URLKEY = 'contenturl'
    url = models.URLField(blank=False)
    
    @classmethod
    def getor(cls,request):
        title = cls.getTitle(request)
        url = cls.getURL(request)
        geopt = GeoPt.getor(request)
        return getOrCreate(cls,title=title, url = url, geopt = geopt)

    @classmethod
    def getURL(cls, request):
        return getVal(request, cls.URLKEY)


class UserContent(ScenicContent):
    user = models.ForeignKey(User)

    



class UserPicture(UserContent):

    @staticmethod
    def get_image_path(instance, filename):
        return os.path.join('photos',str(instance.id),filename)



    picture = models.ImageField(upload_to=get_image_path,blank=False)
    IMG_KEY = 'image'


    @classmethod
    def putPhoto(cls, request):
        photo = cls.getor(request)
        image = cls.getImage(request)
        photo.picture.save(image.name, image)

    @classmethod
    def getImage(cls,request):
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                return request.FILES[IMG_KEY]

class UserComment(UserContent):
    comment = models.TextField()


class ContentRating(models.Model):
    user = models.ForeignKey(User)
    content = models.ForeignKey(ScenicContent)
    rating = models.IntegerField(default=0)
    class Meta:
        unique_together = ("user", "content")

    @classmethod
    def getor(cls, content, user):
        return getOrCreate(cls,content = content, user = user)

    @classmethod
    def setRating(cls, content, user, rating):
        cRating = cls.getor(content,user)
        cRating.rating = rating
        cRating.save()
