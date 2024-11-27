# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, AccountSearchView

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')

# URL patterns
urlpatterns = [
    # Include all router-generated URLs
    path('', include(router.urls)),
    
    # Custom search endpoint
    path('accounts/search/', AccountSearchView.as_view(), name='account-search'),
]