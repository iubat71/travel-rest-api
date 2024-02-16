from rest_framework import viewsets,status
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializer import (
   PaymentBookingSerializer
)
import stripe

from .models import StripePayment
from rest_framework.response import Response


class PaymentBookingViewSet(viewsets.ModelViewSet):
    queryset = PaymentBooking.objects.all()
    serializer_class = PaymentBookingSerializer

    @action(methods=["GET"], detail=False, url_path="payable")
    def get_payable(self, request):
        user = request.user
        payable_orders = PaymentBooking.objects.filter(user=user, payment_status=False)
        serialized_orders = PaymentBookingSerializer(payable_orders, many=True).data
        return Response(serialized_orders)

    @action(methods=["POST"], detail=False, url_path="pay_stripe")
    def pay_stripe(self, request, *args, **kwargs):
        try:
            api_key = StripePayment.objects.first().api_key

            total_amount = request.data.get("amount")
            stripe.api_key = api_key
            success_url = 'http://127.0.0.1:8000/?total_payable={}'.format(total_amount)
            cancel_url = 'http://127.0.0.1:8000/api/restaurant/payments/payable/'

            line_items_data = [
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(float(total_amount) * 100),
                        "product_data": {
                            "name": "Your Bill",
                        },
                    },
                    "quantity": 1,
                }]
            session_data = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items_data,
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )

            if session_data:
                payment = PaymentBooking.objects.create(booking=None, payment_status=False)
                return Response(
                    {
                        "checkout_url": session_data.url,
                        "session_data": session_data,
                        "payment_id": payment.id  
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)