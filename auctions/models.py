from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=200)
    bid = models.CharField(max_length=10)
    image = models.ImageField(default='No Image', upload_to='images')

    def __str__(self):
        return (f'{self.title}, {self.description}, {self.bid}')



class Bids(models.Model):
    pass

class Comments(models.Model):
    pass


