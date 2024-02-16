from django.db import models
from travel_app.models import *
# Create your models here.

class StripePayment(models.Model):
    api_key=models.CharField(max_length=1000)
    def save(self, *args, **kwargs):
        if not self.pk and StripePayment.objects.exists():
            return
        super().save(*args, **kwargs)
        
class PaymentBooking(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Order {self.booking.id}"