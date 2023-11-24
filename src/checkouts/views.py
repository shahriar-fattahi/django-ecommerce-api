from rest_framework import views, permissions, response
from .permissions import IsCheckOut
from orders.models import Order
from . import models
from users import authentication
import requests
import json
from django.conf import settings

ZP_API_REQUEST = "https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"
CallbackURL = "http://127.0.0.1:8080/verify/"


class OrderPayView(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, order_id):
        try:
            order = Order.objects.get(
                id=int(order_id), user_id=int(request.user.id), paid=False
            )
        except Order.DoesNotExist:
            return response.Response({"Exception": "Order Not Found'"})

        request.session["order_pay"] = {
            "order_id": order.id,
        }
        models.Checkout.objects.create(
            user=request.user, order=order, is_completed=False
        )
        description = f"payment order No.{order.id}"
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.get_total_price(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {
                "mobile": self.request.user.phone,
                "email": self.request.user.email,
            },
        }
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req = requests.post(
            url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header
        )
        authority = req.json()["data"]["authority"]
        if len(req.json()["errors"]) == 0:
            url_resp = ZP_API_STARTPAY.format(authority=authority)
            return response.Response({"url": url_resp})
        else:
            e_code = req.json()["errors"]["code"]
            e_message = req.json()["errors"]["message"]
            return response.Response(
                f"Error code: {e_code}, Error Message: {e_message}"
            )


class PaymentVerifyView(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (IsCheckOut,)

    def get(self, request):
        order_id = int(request.session["order_pay"]["order_id"])
        try:
            order = Order.objects.get(
                id=int(order_id), user_id=int(request.user.id), paid=False
            )
        except Order.DoesNotExist:
            return response.Response({"Exception": "Order Not Found'"})
        checkout = models.Checkout.objects.get(
            user=request.user, order=order, is_completed=False
        )
        payment = models.Payment(checkout=checkout, payment_method="z")
        t_status = request.GET.get("Status")
        t_authority = request.GET["Authority"]
        if request.GET.get("Status") == "OK":
            req_header = {
                "accept": "application/json",
                "content-type": "application/json'",
            }
            req_data = {
                "merchant_id": settings.MERCHANT,
                "amount": order.get_total_price(),
                "authority": t_authority,
            }
            req = requests.post(
                url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header
            )
            if len(req.json()["errors"]) == 0:
                t_status = req.json()["data"]["code"]
                if t_status == 100:
                    order.paid = True
                    order.save()
                    checkout.is_completed = True
                    checkout.save()
                    payment.payment_status = "s"
                    payment.save()
                    del request.session["order_pay"]
                    message = "Transaction success.\nRefID: " + str(
                        req.json()["data"]["ref_id"]
                    )
                    return response.Response({"message": message})
                elif t_status == 101:
                    message = "Transaction submitted : " + str(
                        req.json()["data"]["message"]
                    )
                    return response.Response({"message": message})
                else:
                    return response.Response(
                        "Transaction failed.\nStatus: "
                        + str(req.json()["data"]["message"])
                    )
            else:
                e_code = req.json()["errors"]["code"]
                e_message = req.json()["errors"]["message"]
                message = f"Error code: {e_code}, Error Message: {e_message}"
                return response.Response({"message": message})
        else:
            return response.Response(
                {"message": "Transaction failed or canceled by user"}
            )
