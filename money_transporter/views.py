from django.db.models import Q
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from money_transporter import serializers as ser, models
from money_transporter.models import Transaction
from money_transporter.services import MoneyTransfer


class CreateUserView(GenericAPIView):
    """Регистрация нового пользователя"""
    serializer_class = ser.CreateUserSerializer
    queryset = models.User
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.queryset.objects.create_user(**serializer.validated_data)
        return_data = serializer.data
        return_data.pop('password')

        return Response(return_data, status=status.HTTP_201_CREATED)


class CurrencyListView(ListAPIView):
    """Получение списка доступных валют"""
    serializer_class = ser.CurrencySerializer
    queryset = models.Currency.objects.all()
    permission_classes = (AllowAny,)


class MakeTransferView(GenericAPIView):
    """Выполнение денежного перевода"""
    serializer_class = ser.MoneyTransferSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender = request.user
        recipient = serializer.validated_data['recipient']
        amount = serializer.validated_data['amount']

        recipient_increase_amount = MoneyTransfer(sender, recipient, amount).make()

        Transaction.objects.create(
            sender=sender,
            recipient=recipient,
            sender_amount=amount,
            recipient_amount=recipient_increase_amount,
            sender_currency=sender.currency,
            recipient_currency=recipient.currency,
        )

        return Response()


class TransactionListView(ListAPIView):
    """Список транзакций, в которых участвует пользователь"""
    serializer_class = ser.TransactionSerializer

    def get_queryset(self):
        return models.Transaction.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ).order_by('-create_datetime')
