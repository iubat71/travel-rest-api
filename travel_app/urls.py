from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  .views import  *
 
# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'airports', AirportsViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'cities', CityViewSet)
router.register(r'countries', CountryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
