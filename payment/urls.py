from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  .views import  *
 
# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'payment', PaymentBookingViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
