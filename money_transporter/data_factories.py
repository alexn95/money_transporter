import random
import string

import factory

from money_transporter import models


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Currency

    symbol = factory.Iterator(list(string.ascii_letters))
    title = factory.Iterator([f'Валюта{number}' for number in range(0, 1000)])
    multiplicity = random.randint(1, 100)
    is_base = False


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Course

    course = random.randint(1, 10)
    currency = factory.SubFactory(CurrencyFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    email = factory.Iterator([f'mail{number}@mail.ru' for number in range(0, 1000)])
    currency = factory.SubFactory(CurrencyFactory)
    balance = 10000.00


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Transaction

    sender = factory.SubFactory(UserFactory)
    recipient = factory.SubFactory(UserFactory)

    sender_currency = factory.SubFactory(CurrencyFactory)
    sender_recipient = factory.SubFactory(CurrencyFactory)
