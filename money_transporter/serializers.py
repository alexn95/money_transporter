from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from money_transporter import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = ('symbol', 'title', 'multiplicity')


class CreateUserSerializer(serializers.ModelSerializer):
    currency = serializers.CharField()

    class Meta:
        model = models.User
        fields = ('email', 'currency', 'balance', 'password')

    def validate(self, attrs):
        """
        Проверяется, что валюта пользователя существет и добавляет ее в атрибуты.
        """

        try:
            currency = models.Currency.objects.get(title=attrs['currency'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Такой валюты нет в базе')

        attrs['currency'] = currency

        return attrs


class MoneyTransferSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    email = serializers.EmailField()

    def validate(self, attrs):
        """
        Проверяется, что:
            у пользователя есть деньги,
            пользователь-адресат с пеереданной почту существует,
            и что пользователь-адресат не является отправителем.

        Отправитель добавляется в атрибуты.
        """

        sender = self.context['request'].user
        if sender.balance <= 0:
            raise serializers.ValidationError('У пользователя нет денег')

        try:
            recipient = models.User.objects.get(email=attrs['email'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Пользователя с такой почтой не существует')

        if recipient == sender:
            raise serializers.ValidationError('Нельзя отправляеть деньги самому себе')

        attrs['recipient'] = recipient

        return attrs


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    sender_currency = serializers.StringRelatedField()
    recipient_currency = serializers.StringRelatedField()

    class Meta:
        model = models.Transaction
        fields = (
            'sender', 'recipient', 'sender_amount', 'recipient_amount', 'sender_currency',
            'recipient_currency', 'create_datetime'
        )
