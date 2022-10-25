from django.forms import ModelForm
from django import forms
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'price', 'category', 'image']

class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['user', 'listing', 'bid']
        

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['commment']
        labels = {
            "commment": "Leave a comment"
        }




