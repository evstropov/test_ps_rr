from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from finance.exceptions import PaymentAlreadyProcessedError
from finance.payment_systems import BankPaymentHandler
from finance.serializers import BankPaymentWebhookSerializer


class BankPaymentWebhookAPIView(APIView):

    def post(self, request):
        serializer = BankPaymentWebhookSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                bank_handler = BankPaymentHandler(payload=data, wallet_id=serializer.wallet_id)
                bank_handler.process()
            except PaymentAlreadyProcessedError:
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
