from django.contrib.gis.db import models
#from django.db import models
import os
from django.forms import Form as PhotoForm
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point


def getOrCreate(cls, **kwargs):
    return cls.objects.get_or_create(**kwargs)[0]

def getVal(request,key):
    try:
        result = request.GET[key]
        if isinstance(result,str) or isinstance(result,unicode):
            return result
        result =  result[0]
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

    def toDic(self):
        dic = {}
        dic[GeoPt.LATKEY] = self.lat
        dic[GeoPt.LNGKEY] = self.lng
        return dic

    
    
    @classmethod
    def getor(cls,request):
        lat = cls.getLat(request)
        lng = cls.getLng(request)
        return getOrCreate(cls,lat=lat, lng = lng)

    def toPoint(self):
        return Point(self.lat,self.lng)

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

    def toDic(self):
        return self.device_id

    
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
    COORD_KEY = 'coord'
    DATE_KEY = 'date'
    POINT_KEY = 'point'
    
    title = models.CharField(max_length=200)
    geopt = models.ForeignKey(GeoPt, related_name='%(app_label)s_%(class)s_related')
    date = models.DateTimeField(auto_now=True)
    point = models.PointField()
    objects = models.GeoManager()
    
    def toDic(self):
        dic = {}
        dic[ScenicContent.TITLEKEY] = self.title
        dic[ScenicContent.COORD_KEY] = self.geopt.toDic()
        dic[ScenicContent.DATE_KEY] = str(self.date)
        return dic

    @classmethod
    def getor(cls,request):
        content = getOrCreate(cls, **cls.getkwargs(request))
        return content

    @classmethod
    def getkwargs(cls,request):
        title = getVal(request,cls.TITLEKEY)
        geopt = GeoPt.getor(request)
        point = geopt.toPoint()
        return {'title':title,'geopt':geopt, 'point': point}
        

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
    USER_KEY = 'user'
    
    @classmethod
    def getor(cls, request):
        kws = cls.getkwargs(request)
        print kws['point']
        content = getOrCreate(cls, **kws)
        print content
        return content

    def toDic(self):
        dic = super(UserContent,self).toDic()
        dic.update({UserContent.USER_KEY: self.user.toDic()})
        return dic
    
    @classmethod
    def getkwargs(cls, request):
        kw = cls.__bases__[0].getkwargs(request)
        kw['user'] = User.getor(request)
        return kw


def get_image_path(instance, filename):
    return os.path.join('photos',str(instance.id),filename)

class UserPicture(UserContent):
    picture = models.ImageField(upload_to=get_image_path,blank=False)
    icon = models.ImageField(upload_to=get_image_path, blank=False)
    magHeading = models.FloatField()
    trueHeading = models.FloatField()
    
    IMG_KEY = 'image'
    ICON_KEY = 'icon'
    SET_KEY = 'photos'
    TRUE_KEY = 'trueheading'
    MAG_KEY = 'magheading'

    def toDic(self):
        dic = super(UserPicture, self).toDic()
        dic.update({UserPicture.IMG_KEY:self.picURL(), UserPicture.ICON_KEY:self.iconURL(), UserPicture.MAG_KEY:self.magHeading, UserPicture.TRUE_KEY:self.trueHeading})
        return dic

    @classmethod
    def around(cls, request):
        n = int(getVal(request, 'npics'))
        km = float(getVal(request, 'km'))
        point = GeoPt.getPoint(request)
        return cls.objects.filter(point__distance_lte=(point,D(km))).order_by('-date')[:n]

    def iconURL(self):
        try:
            return 'http://www.scenicgps.com' + self.icon.url
        except:
            return 'http://www.scenicgps.com/images/video.png'

    def picURL(self):
        return 'http://www.scenicgps.com' + self.picture.url

    @classmethod
    def fetchAllPictures(cls, request):
        pics = cls.objects.order_by('-date')
        return [pic.toDic() for pic in pics]

    @classmethod
    def fetchPictures(cls, request):
        pics = cls.objects.order_by('-date')[:10]
        return [pic.toDic() for pic in pics]

    @classmethod
    def putPhoto(cls, request):
        #content = getOrCreate(cls, **UserPicture.getkwargs(request))
        #content.magHeading = getVal(request, cls.MAG_KEY)
        #content.trueHeading = getVal(request, cls.TRUE_KEY)
        #content.save()
        user = User.getor(request)
        user.save()
        geopt = GeoPt.getor(request)
        geopt.save()
        title = getVal(request, 'title')
        th = getVal(request, 'trueheading')
        mh = getVal(request, 'magheading')
        point = geopt.toPoint()
        content = UserPicture(user = user, geopt = geopt, title = title, point = point, trueHeading = th, magHeading = mh)
        content.save()
        image = cls.getImage(request)
        content.picture.save(image.name, image)
        icon = cls.getIcon(request)
        content.icon.save(icon.name, icon)
        content.save()

    @classmethod
    def getkwargs(cls, request):
        kw = cls.__bases__[0].getkwargs(request)
        kw['magHeading'] = getVal(request,cls.MAG_KEY)
        kw['trueHeading'] = getVal(request,cls.TRUE_KEY)
        return kw

    @classmethod
    def getImage(cls,request):
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                image_file = request.FILES[cls.IMG_KEY]
                return image_file

    @classmethod
    def getIcon(cls,request): 
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                image_file = request.FILES[cls.ICON_KEY]
                return image_file
       
                

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
