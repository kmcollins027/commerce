from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:item_id>", views.listing_page, name="listing_page"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("filtered_listings/<str:selection>", views.filtered_listings, name="filtered_listings"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("api/toggle_watchlist/<int:listing_id>", views.api_toggle_watchlist, name="api-toggle-watchlist"),
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
