from django.forms import ModelForm
from django import forms
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'bid', 'image']


