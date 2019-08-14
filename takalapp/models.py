from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Profile(models.Model):
    full_name = models.CharField(max_length=200,null = True, blank = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    weight = models.CharField(max_length = 200,null = True, blank = True)
    height = models.CharField(max_length = 200,null = True, blank = True)
    age = models.CharField(max_length = 200,null = True, blank = True)
    province = models.CharField(max_length = 200,null = True, blank = True)
    sex = models.CharField(max_length = 200,null = True, blank = True)
    token = models.CharField(max_length=246,unique=True)
    code = models.CharField(max_length=50)
    score = models.CharField(max_length=200,default=0)

    def __str__(self):
        return self.user.username

class Trip(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    startpoint_lat = models.CharField(max_length=200)
    startpoint_lng = models.CharField(max_length=200)
    passeddistance = models.CharField(max_length=200,null=True,blank=True)
    burenedcalory = models.CharField(max_length=200,null=True,blank=True)
    avgspeed = models.CharField(max_length=200,null=True,blank=True)
    score = models.IntegerField(null=True,blank=True)
    endpoint_lat = models.CharField(max_length=200,null=True,blank=True)
    endpoint_lng = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.profile.user.username

class Store(models.Model):
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    store_lat = models.CharField(max_length=200)
    store_lng = models.CharField(max_length=200)
    score = models.IntegerField()
    phone = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name="نام")
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    score = models.CharField(max_length=200, verbose_name="امتیاز مورد نیاز")
    image = models.ImageField(upload_to="images/", verbose_name="تصویر محصول")

    def __str__(self):
        return self.name

class Offer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نام کاربری")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True, verbose_name="محصول")
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="فروشگاه")
    number = models.IntegerField(default=1, verbose_name="تعداد")
    date = models.DateField(auto_now_add=True, verbose_name="تاریخ")
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('offer', args=[str(self.id)])
