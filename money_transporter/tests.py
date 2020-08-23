import datetime
from random import randint

from django.test import TestCase

from money_transporter.data_factories import CourseFactory, UserFactory, CurrencyFactory
from money_transporter.models import Currency, Course
from money_transporter.services import MoneyTransfer


class MoneyTransferServiceTestCase(TestCase):
    """Тестируется сервис перевода денег"""

    def _check_balance(self, user, expected_balance):
        """Сравнивается ожидаемый баланс с актуальным"""
        user.refresh_from_db()
        self.assertAlmostEquals(user.balance, expected_balance, places=2)


class MoneyTransferSameCurrencyTestCase(MoneyTransferServiceTestCase):
    """Тестируется перевод денег пользователю с валютой, отличной от валюты отправителя"""

    @classmethod
    def setUpTestData(cls):
        course = CourseFactory()
        cls.sender = UserFactory(currency=course.currency)
        cls.recipient = UserFactory(currency=course.currency)

    def test_1_default_transfer(self):
        """Перевод с положительным счетом отправителя в результате"""
        MoneyTransfer(self.sender, self.recipient, 5000).make()
        self._check_balance(self.sender, 5000)
        self._check_balance(self.recipient, 15000)

    def test_2_transfer_lead_negative_balance(self):
        """Перевод с отрицательным счетом отправителя в результате"""
        MoneyTransfer(self.sender, self.recipient, 6000).make()
        self._check_balance(self.sender, -1000)
        self._check_balance(self.recipient, 21000)

    def test_3_transfer_to_negative_balance(self):
        """Перевод на счет с отрицательным балансом"""
        MoneyTransfer(self.recipient, self.sender, 1001).make()
        self._check_balance(self.sender, 1)
        self._check_balance(self.recipient, 19999)


class MoneyTransferDiffCurrencyTestCase(MoneyTransferServiceTestCase):
    """Тестируется перевод денег пользователю с валютой, отличной от валюты отправителя"""

    @staticmethod
    def _create_user_with_currency(course_value, multiplicity):
        """Создаются пользователь, валюта и курс с переданными параметрами"""
        user = UserFactory(currency__multiplicity=multiplicity)
        course = CourseFactory(currency=user.currency, course=course_value)
        return user, course

    @staticmethod
    def _calc_coefficient(sender_course, sender_multiplicity, recipient_course, recipient_multiplicity):
        return (sender_multiplicity * recipient_course) / (recipient_multiplicity * sender_course)

    def _make_test(self, sender_course, sender_multiplicity, recipient_course, recipient_multiplicity,
                   recipient_balance_increase):
        """
        Создаются пользователь, валюта и курс с переданными параметрами, выполняется
        перевод и проверяется баланс на счетах в результате перевода.
        """

        sender, sender_course = self._create_user_with_currency(sender_course, sender_multiplicity)
        recipient, recipient_course = self._create_user_with_currency(recipient_course, recipient_multiplicity)
        MoneyTransfer(sender, recipient, 1000).make()

        self._check_balance(sender, 9000)
        self._check_balance(recipient, 10000 + recipient_balance_increase)

    def test_money_transfer_random_courses(self):
        """Выполняются тесты со случайно сгенерированными параметрами валют"""
        for i in range(0, 1):
            course_data = randint(1, 100), randint(1, 100), randint(1, 100), randint(1, 100)
            self._make_test(*course_data, self._calc_coefficient(*course_data) * 1000)


class TestManagers(TestCase):

    def test_currency_manager(self):
        """Проверяется менеджер валюты на получение актуального курса"""

        currency = CurrencyFactory()
        CourseFactory(currency=currency)
        CourseFactory(currency=currency)
        CourseFactory(currency=currency, start_datetime=(datetime.datetime.now() + datetime.timedelta(hours=1)))
        actual_course = CourseFactory(currency=currency)

        self.assertEqual(Course.objects.count(), 4)
        self.assertEqual(Currency.objects.first().actual_course, actual_course)
