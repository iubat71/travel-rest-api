from rest_framework import serializers
from .models import PaymentBooking

class PaymentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentBooking
        fields = ['id', 'booking', 'payment_status']