from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal



class User(AbstractUser):
    pass

class Listings(models.Model):

    CATEGORY_CHOICES = [
    ('MS', 'Motors'),
    ('ECCS', 'Electronics'),
    ('C_ART', 'Collectibles & Art'),
    ('CLOTH', 'Clothing & Accessories'),
    ('BUSS', 'Business & Industrial'),
    ('HG', 'Home & Garden'),
    ('SPORT', 'Sporting Goods'),
    ('JE', 'Jewelry & Watches'),
    ('OT', 'Other'),
    ]

    MOTORS = 'MS'
    ELECTRONICS = 'ECCS'
    COLLECTIBLES_ART = 'C_ART'
    CLOTHING_ACC = 'CLOTH'
    BUSINESS_IND = 'BUSS'
    HOME_GARDEN = 'HG'
    SPORTING = 'SPORT'
    JEWELRY = 'JE'
    OTHER = 'OT'
    

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=200)
    price = models.PositiveSmallIntegerField(default=0)
    highestbid = models.PositiveSmallIntegerField(default=0, blank=True)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default='MOTORS')
    active = models.BooleanField(default=True)
    image = models.ImageField(default='No Image', upload_to='images')

    def __str__(self):
        return (f'{self.title}, {self.description}, {self.price}')
    
    class Meta:
        verbose_name_plural = "Listings"



class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)
    bid = models.PositiveSmallIntegerField()

    def __str__(self):
        return (f'{self.user}, {self.listing}, {self.bid}')

    class Meta:
        verbose_name_plural = "Bids"


class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    commment = models.TextField(blank=True, max_length=200)
    timestamp = models.DateTimeField(default=None, auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Comments"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='watch_active')
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} + {self.listing}'



