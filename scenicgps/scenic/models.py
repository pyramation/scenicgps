from django.db import models
import os
from django.forms import Form as PhotoForm
from geohash import Geohash
def getOrCreate(cls, **kwargs):
    return cls.objects.get_or_create(**kwargs)[0]

def getVal(request,key):
    try:
        result = request.GET[key]
        if isinstance(result,str) or isinstance(result,unicode):
            return result
        result =  result[0]
        asdfasd
    except:
        return None

def getRating(request):
    KEY = 'rating'
    return int(getVal(request,KEY))



# Create your models here.
class GeoPt(models.Model):
    LATKEY = 'lat'
    LNGKEY = 'lng'
    HASH_KEY = 'hash'
    lat = models.FloatField()
    lng = models.FloatField()
    geohash = models.CharField(max_length = 50)
    
    def geoHash(self):
        return str(Geohash((self.lat, self.lng)))

    def toDic(self):
        dic = {}
        dic[GeoPt.LATKEY] = self.lat
        dic[GeoPt.LNGKEY] = self.lng
        return dic
    
    @classmethod
    def getor(cls,request):
        pt =  getOrCreate(cls,lat=cls.getLat(request),lng=cls.getLng(request))
        pt.geohash = pt.geoHash()
        pt.save()
        return pt

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
    title = models.CharField(max_length=200)
    geopt = models.ForeignKey(GeoPt, related_name='%(app_label)s_%(class)s_related')
    date = models.DateTimeField(auto_now = True)

    def toDic(self):
        dic = {}
        dic[ScenicContent.TITLEKEY] = self.title
        dic[ScenicContent.COORD_KEY] = self.geopt.toDic()
        return dic

    @classmethod
    def getor(cls,request):
        
        content = getOrCreate(cls, **cls.getkwargs(request))
        return content

    @classmethod
    def getkwargs(cls,request):
        title = getVal(request,cls.TITLEKEY)
        geopt = GeoPt.getor(request)
        return {'title':title,'geopt':geopt}
        

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
        user = User.getor(request)
        content = getOrCreate(cls, **ScenicContent.getkwargs(request))
        content.user = user
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
        dic.update({UserPicture.IMG_KEY:self.picURL(), UserPicture.ICON_KEY:self.iconURL(),UserPicture.MAG_KEY:self.magHeading, UserPicture.TRUE_KEY:self.trueHeading})
        return dic

    def iconURL(self):
        try:
            return 'http://www.scenicgps.com' + self.icon.url
        except:
            return 'http://www.scenicgps.com/images/video.png'

    def picURL(self):
        return 'http://www.scenicgps.com' + self.picture.url

    @classmethod
    def fetchAllPictures(cls, request):
        pics = cls.objects.all()
        return [pic.toDic() for pic in pics]

    @classmethod
    def nearby(cls, request):
        n = int(getVal(request,'npics'))
        checkhash = getVal(request,'geohash')
        
        while len(checkhash) > 0:
            pics = cls.objects.filter(geopt__geohash__contains=checkhash)
            if len(pics) >= n:
                return pics[:n]
            checkhash = checkhash[:-1]
        return cls.objects.all()
            
    @classmethod
    def fetchPictures(cls, request):
        pics = cls.objects.all()[:10]
        return [pic.toDic() for pic in pics]

    @classmethod
    def putPhoto(cls, request):
        content = getOrCreate(cls, **cls.getkwargs(request))
        image = cls.getImage(request)
        icon = cls.getIcon(request)
        content.save()
        content.picture.save(image.name, image)
        content.icon.save(icon.name, icon)
        content.save()

    @classmethod
    def getkwargs(cls, request):
        kw = cls.__bases__[0].getkwargs(request)
        kw['magHeading'] = float(getVal(request,cls.MAG_KEY))
        kw['trueHeading'] = float(getVal(request,cls.TRUE_KEY))
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
