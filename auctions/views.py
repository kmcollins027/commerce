from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import *
from .forms import *

@login_required(login_url='login')
def index(request):
    user_list = []
    listings = Listings.objects.filter(active=1)
    watching = Watchlist.objects.filter(user=request.user)
    page = request.POST.get('page', 1)

    paginator = Paginator(listings, 5)

    listing_pages = paginator.page(page)

    for w in watching:
        user_list.append(w.listing)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "length": len(listings),
        "user_list": user_list,
        "listing_pages": listing_pages
    })

@login_required(login_url='login')
def index_pagination(request, pages):
    user_list = []
    listings = Listings.objects.filter(active=1)
    watching = Watchlist.objects.filter(user=request.user)
    page = pages

    paginator = Paginator(listings, 5)

    listing_pages = paginator.page(page)

    for w in watching:
        user_list.append(w.listing)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "length": len(listings),
        "user_list": user_list,
        "listing_pages": listing_pages
    })




@login_required(login_url='login')
def closed_listings(request):
    winners = []
    listings = Listings.objects.filter(active=0)
    for listing in listings:
        winner = Bids.objects.filter(listing_id=listing.id).last()
        winners.append(winner)
    zipped = zip(listings, winners)

    return render(request, "auctions/closed_listings.html", {
        "listings": listings,
        "length": len(listings),
        "winners": winners,
        "zipped": zipped,
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
            instance.user = request.user
            instance.save()
            return redirect('index')
        else:
            return render(request, "auctions/create_listing.html", {"list_form": list_form})
    else:
        return render(request, "auctions/create_listing.html", {"list_form": ListingForm()})

def api_toggle_watchlist(request, listing_id):
    if request.method == "POST":
        if not Watchlist.objects.filter(user_id=request.user.id, listing_id=listing_id).exists():
            w = Watchlist.objects.create(user=request.user, listing=Listings.objects.get(pk=listing_id), active=True)
            return JsonResponse({"current_status": "on"})
        else:
            watchlist = Watchlist.objects.get(user_id=request.user.id, listing_id=listing_id)
            if watchlist.active == False:
                watchlist.active = True
                watchlist.save(update_fields=["active"])
            
                return JsonResponse({"current_status": "on"})
            if watchlist.active == True:
                watchlist.active = False
                watchlist.save(update_fields=["active"])
                
                return JsonResponse({"current_status": "off"})
            return JsonResponse({'error': 'something went wrong'})
    
@login_required(login_url='login') 
def listing_page(request, item_id):
    if request.method == "POST":
        if "watch" in request.POST:
            if not Watchlist.objects.filter(user_id=request.user.id, listing_id=item_id).exists():
                w = Watchlist.objects.create(user=request.user, listing=Listings.objects.get(pk=item_id), active=True)
                
                return HttpResponseRedirect(reverse("listing_page", args=(item_id,)))
            else:
                watchlist = Watchlist.objects.get(user_id=request.user.id, listing_id=item_id)
                watchlist.active = True
                watchlist.save(update_fields=["active"])
                return HttpResponseRedirect(reverse("listing_page", args=(item_id,)))
                
        if "unwatch" in request.POST:
            watchlist = Watchlist.objects.get(user_id=request.user.id, listing_id=item_id)
            watchlist.active = False
            watchlist.save(update_fields=["active"])
            watching = Watchlist.objects.get(user_id=request.user.id, listing_id=item_id)
            return HttpResponseRedirect(reverse("listing_page", args=(item_id,)))

        if "comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.user = request.user
                instance.listing_id = item_id
                instance.timestamp = timezone.localtime()
                instance.save()
                return HttpResponseRedirect(reverse("listing_page", args=(item_id,)))

        if "bid" in request.POST:
            listing = Listings.objects.get(pk=item_id)
            price = listing.price
            bid = int(request.POST.get("amount"))
            try:
                highest = Bids(user_id=request.user.id, listing_id=item_id).last()
            except:
                highest = 0
            if bid < price and bid <= highest:
                return render(request, "auctions/listing.html", {
                    "error_message": "Bidding price must be greater than current price"
                })
            else:
                bids = Bids(user_id=request.user.id, listing_id=item_id, bid=bid)
                bids.save()
                highestbid = Listings.objects.get(pk=item_id)
                highestbid.highestbid = bid
                highestbid.save(update_fields=["highestbid"])
                return HttpResponseRedirect(reverse("listing_page", args=(item_id,)))

        if "close" in request.POST:
            listing = Listings.objects.get(pk=item_id)
            listing.active = False
            listing.save(update_fields=["active"])
            return HttpResponseRedirect(reverse("index"))

    else:
        try:
            watching = Watchlist.objects.get(user_id=request.user.id, listing_id=item_id)
        except:
            watching = None
        try:
            bids = Bids.objects.filter(listing_id=item_id)
        except:
            bids = 0
        try:
            listing = Listings.objects.get(pk=item_id)
            winner = Bids.objects.filter(listing_id=item_id).last()
        except:
            winner = None

        return render(request, "auctions/listing_page.html", {
            "total_bids": len(bids),
            "bid": bids,
            "winner": winner,
            "listing": Listings.objects.get(pk=item_id),
            "watching": watching,
            "watchlist": len(Watchlist.objects.filter(user_id=request.user.id)),
            "comments": Comments.objects.filter(listing_id=item_id),
            "comment_form": CommentForm(),
            "user": request.user
        })

@login_required(login_url='login') 
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listings.CATEGORY_CHOICES
    })

@login_required(login_url='login') 
def watchlist(request):
    try:
        watchlist = Watchlist.objects.filter(user_id=request.user.id, active=True).values_list("listing_id")
        watching = Listings.objects.filter(id__in = watchlist)
    except:
        watching = 0
    return render(request, "auctions/watchlist.html", {
        "watching": watching,
        "watchlist": len(Watchlist.objects.filter(user_id=request.user.id))
        })

@login_required(login_url='login') 
def filtered_listings(request, selection):
    if selection == 'Motors': 
        choice = 'MS'
    if selection == 'Electronics':
        choice = 'ECCS'
    if selection == 'Collectibles & Art': 
        choice = 'C_ART'
    if selection == 'Clothing & Accessories': 
        choice = 'CLOTH'
    if selection == 'Business & Industrial': 
        choice = 'BUSS'
    if selection == 'Home & Garden': 
        choice = 'HG'
    if selection == 'Sporting Goods': 
        choice = 'SPORT'
    if selection == 'Jewelry & Watches': 
        choice = 'JE'
    if selection == 'Other': 
        choice = 'OT'

    filtered = Listings.objects.filter(category=choice, active=1)

    listify = list(filtered)
    for listing in listify:
        if listing.active == 0:
            listify.remove(listing)

    return render(request, "auctions/filtered_listings.html", {
        "filtered": filtered,
        "selection": selection,
        "length": len(filtered)
    })