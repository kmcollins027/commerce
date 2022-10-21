from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

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

class User(AbstractUser):
    pass

class Listings(models.Model):
    MOTORS = 'MS'
    ELECTRONICS = 'ECCS'
    COLLECTIBLES_ART = 'C_ART'
    CLOTHING_ACC = 'CLOTH'
    BUSINESS_IND = 'BUSS'
    HOME_GARDEN = 'HG'
    SPORTING = 'SPORT'
    JEWELRY = 'JE'
    OTHER = 'OT'
    

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=200)
    bid = models.DecimalField(default=Decimal('0.00'), max_digits=5, decimal_places=2)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default='MOTORS')
    image = models.ImageField(default='No Image', upload_to='images')

    def __str__(self):
        return (f'{self.title}, {self.description}, {self.bid}')
    
    class Meta:
        verbose_name_plural = "Listings"



class Bids(models.Model):
    bid_user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    bid_listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)
    bid_amount = models.DecimalField(default=Decimal('0.00'), max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Bids"


class Comments(models.Model):
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    commment = models.TextField(blank=True, max_length=200)

    class Meta:
        verbose_name_plural = "Comments"

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.user_id} + {self.listing_id}'



