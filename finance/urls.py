from django.urls import path

from finance.views import BankPaymentWebhookAPIView

urlpatterns = [
    path('bank/', BankPaymentWebhookAPIView.as_view()),
]
