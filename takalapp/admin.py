from django.contrib import admin
from . import models
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','age',)

admin.site.register(models.Profile, ProfileAdmin)

class TripAdmin(admin.ModelAdmin):
    list_display = ('profile','date',)

admin.site.register(models.Trip, TripAdmin)
