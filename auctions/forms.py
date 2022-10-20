from django.forms import ModelForm
from django import forms
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'bid', 'category', 'image']

class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['bid_user_id', 'bid_listing', 'bid_amount']
        

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['listing_id', 'user_id', 'commment']




