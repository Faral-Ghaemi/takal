from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic.list import ListView
from . import models
from django.template import loader
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer
from kavenegar import *
from django.views.decorators.csrf import csrf_exempt
import hashlib
from random import randrange
from datetime import date, timedelta
from django.db.models import Avg, Count, Min, Sum
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
# Create your views here.

@login_required(login_url='/login/')
def admin(request):
    today = date.today()

    trips = models.Trip.objects.all()
    onlinetrips = models.Trip.objects.filter(endpoint_lat__isnull=True)
    todaytrips = models.Trip.objects.filter(date=today)
    day1= models.Trip.objects.filter(date=today - timedelta(days=1))
    day2= models.Trip.objects.filter(date=today - timedelta(days=2))
    day3= models.Trip.objects.filter(date=today - timedelta(days=3))
    day4= models.Trip.objects.filter(date=today - timedelta(days=4))
    profiles=models.Profile.objects.all()
    sum=models.Profile.objects.annotate(Count('score'))
    users = User.objects.all().count()
    username = request.user.username

    stores = models.Store.objects.all()
    offers = models.Offer.objects.filter()
    todayoffers = models.Offer.objects.filter(date=today)
    products = models.Product.objects.all()

    lasttrips = models.Trip.objects.filter(endpoint_lat__isnull=False).order_by('-id')[:4]
    context = {
        'lasttrips': lasttrips,
        'todayoffers': todayoffers,
        'products': products,
        'offers': offers,
        'stores': stores,
        'todaytrips': todaytrips,
        'day1' : day1,
        'day2' : day2,
        'day3' : day3,
        'day4' : day4,
        'username': username,
        'users': users,
        'trips' : trips,
        'today': today,
        'scores': sum,
        'onlinetrips': onlinetrips,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context,request))

@csrf_exempt
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/a/')
    return render_to_response('login.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username1 = request.POST.get('phone')
        try:
            user1 = User.objects.get(username=username1)
            profile = models.Profile.objects.get(user=user1)
            token = profile.token
            if profile.full_name is None:
                code = randrange(1000,9999)
                user1 = User.objects.get(username=username1)
                api = KavenegarAPI('7279477839674A4370504F4D4B5547426A6B676E38347A32464F3430766A7841')
                params = { 'sender' : '1000596446', 'receptor': username1, 'message' :'کاربر گرامی تکل، ضمن خوش آمدگویی، رمز یکبار مصرف شما '+str(code)+'می باشد ' }
                response = api.sms_send( params)
                return JsonResponse({'token': token,'code': code,'mode': 0,})
            full_name = profile.full_name
            weight = profile.weight
            height = profile.height
            age = profile.age
            province1 = profile.province
            if province1 == "Tehran":
                province = "1"
            elif province1 == "Qazvin":
                province = "0"
            sex = profile.sex
            score = profile.score
            code1 = randrange(1000,9999)
            profile.code = code1
            profile.save()
            api = KavenegarAPI('7279477839674A4370504F4D4B5547426A6B676E38347A32464F3430766A7841')
            params = { 'sender' : '1000596446', 'receptor': username1, 'message' :'کاربر گرامی تکل، ضمن خوش آمدگویی، رمز یکبار مصرف شما '+str(code1)+' می باشد ' }
            response = api.sms_send( params)
            return JsonResponse({'token': token,'code': code1,'mode': 1,'full_name': full_name,'weight': weight,'height': height,'age':age,'province': province,'sex':sex,'score':score})

        except User.DoesNotExist:
            user = User.objects.create_user(username=username1)
            token1 = hashlib.md5(username1.encode())
            token = token1.hexdigest()
            code = randrange(1000,9999)
            user.save()
            user1 = User.objects.get(username=username1)
            profile = models.Profile.objects.create(user=user1,code=code,token=token)
            profile.save()
            api = KavenegarAPI('7279477839674A4370504F4D4B5547426A6B676E38347A32464F3430766A7841')
            params = { 'sender' : '1000596446', 'receptor': username1, 'message' :'کاربر گرامی تکل، ضمن خوش آمدگویی، رمز یکبار مصرف شما '+str(code)+'می باشد ' }
            response = api.sms_send( params)
            return JsonResponse({'token': token,'code': code,'mode': 0,})
    else :
        return HttpResponse("not post")

@csrf_exempt
def profile(request):
    if request.method == 'POST':
        form = request.POST
        token = form.get('token')
        try:
            profile = models.Profile.objects.get(token=token)

            profile.full_name = form.get('full_name')
            profile.weight = form.get('weight')
            profile.height = form.get('height')
            profile.age = form.get('age')
            if form.get('province') == "1":
                profile.province = "Tehran"
            elif form.get('province') == "0":
                profile.province = "Qazvin"
            profile.sex = form.get('sex')
            profile.save()
            return JsonResponse({'status': 1,})
        except models.Profile.DoesNotExist:
            return JsonResponse({'status': 0,})

@csrf_exempt
def trips(request):
    if request.method == 'POST':
        form = request.POST
        token = form.get('token')
        try:
            profile = models.Profile.objects.get(token=token)
            startpoint_lat = form.get('startpoint_lat')
            startpoint_lng = form.get('startpoint_lng')

            trip = models.Trip.objects.create(profile=profile,startpoint_lat=startpoint_lat,startpoint_lng=startpoint_lng)
            trip.save()
            return JsonResponse({'status': 1,})
        except models.Profile.DoesNotExist:
            return JsonResponse({'status': 0,})





class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
