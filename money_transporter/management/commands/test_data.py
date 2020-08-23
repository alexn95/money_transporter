from django.core.management import BaseCommand

from money_transporter.models import Currency, Course, User


class Command(BaseCommand):
    help = 'Создаються тестовые данные'

    def handle(self, *args, **options):
        """
        Создаются тестовые данные, минимально необходимые для использования приложения.
        Пользователи, валюты, курсы валют.
        """

        currency_base, _ = Currency.objects.get_or_create(symbol='руб.', title='Рубль', multiplicity=1, is_base=True)
        Course.objects.get_or_create(currency=currency_base, course=1)

        # Допустим 100 рублям соответствует 2 доллара
        currency1, _ = Currency.objects.get_or_create(symbol='$', title='Доллар', multiplicity=100)
        course_value = 2 * currency1.multiplicity / 100
        Course.objects.get_or_create(currency=currency1, course=course_value)

        # Допустим 100 рублям соответствует 15 евро
        currency2, _ = Currency.objects.get_or_create(symbol='€', title='Еворо ', multiplicity=1)
        course_value = 15 * currency2.multiplicity / 100
        Course.objects.get_or_create(currency=currency2, course=course_value)

        # Допустим 100 рублям соответствует 50 фунтов
        currency3, _ = Currency.objects.get_or_create(symbol='GPB', title='Фунт ', multiplicity=10)
        course_value = 50 * currency3.multiplicity / 100
        Course.objects.get_or_create(currency=currency3, course=course_value)

        # Допустим 100 рублям соответствует 1 биткоин
        currency4, _ = Currency.objects.get_or_create(symbol='BTC', title='Биткоин ', multiplicity=1)
        course_value = 1 * currency4.multiplicity / 100
        Course.objects.get_or_create(currency=currency4, course=course_value)

        User.objects.create_superuser('superuser@mail.ru', 'password', balance=1000, currency=currency_base)
        User.objects.create_user('user_one@mail.ru', 'password', balance=1000, currency=currency1)
        User.objects.create_user('user_two@mail.ru', 'password', balance=1000, currency=currency2)
