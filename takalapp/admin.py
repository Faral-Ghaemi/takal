from django.contrib import admin
from . import models
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','age',)

admin.site.register(models.Profile, ProfileAdmin)

class TripAdmin(admin.ModelAdmin):
    list_display = ('profile','date',)

admin.site.register(models.Trip, TripAdmin)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'score')

@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('profile', 'product', 'store', 'score')

@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner','score')
