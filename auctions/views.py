from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import *
from .forms import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()

    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login') 
def create_listing(request):
    if request.method == "POST":
        list_form = ListingForm(request.POST, request.FILES)
        if list_form.is_valid():
            instance = list_form.save(commit=False)
            instance.user_id = request.user
            instance.save()
            return redirect('index')
        else:
            return render(request, "auctions/create_listing.html", {"list_form": list_form})
    else:
        return render(request, "auctions/create_listing.html", {"list_form": ListingForm()})
    

def listing_page(request, listing):
    listings = Listings.objects.all()
    return render(request, "auctions/listing_page.html", {
        "listing": listing, "listings": listings
    })

def categories(request):
    return render(request, "auctions/categories.html")


def watchlist(request):
    watchlists = Watchlist.objects.all()
    return render(request, "auctions/watchlist.html", {"watchlists": watchlists})


def add_watchlist(request, listing_id):
    listing = get_object_or_404(Listings, pk=listing_id)
    obj, create = Watchlist.objects.get_or_create(user_id=request.user, listing_id=listing)
    if create:
        Watchlist.objects.create(user_id=request.user, listing_id=listing)
        return redirect('watchlist')
        

    else:
        return render(request, "auctions/listing_page.html", {"err_msg": f"{listing.title} is already on watchlist"})
    #listing_id = listing_id
    #user_id = request.user
    #if request.method == "POST":
        #watchlist_add = Watchlist(user_id = request.user, listing_id = request.listing)
        #watchlist_add.save()
        #return redirect('watchlist')
    
    #else:
        #context = {
        #"listing": listing_id,
        #"user_id": user_id
        #}
        #return render(request, "auctions/add_watchlist.html", context)