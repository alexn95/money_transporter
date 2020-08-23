from django.core.management import BaseCommand

from money_transporter.models import Currency, Course, User


class Command(BaseCommand):
    help = 'Создаються тестовые данные'

    def handle(self, *args, **options):
        """
        Создаються тестовые данные, минимально необходимые для использования приложения.
        Пользователи, валюты, курсы валют.
        """

        currency_base, _ = Currency.objects.get_or_create(symbol='руб.', title='Рубль', multiplicity=1, is_base=True)
        currency_one, _ = Currency.objects.get_or_create(symbol='$', title='Доллар', multiplicity=100)
        currency_two, _ = Currency.objects.get_or_create(symbol='€', title='Еворо ', multiplicity=1)

        # Создается курс для базовой валюты - рубля
        Course.objects.get_or_create(currency=currency_base, course=1)

        # Допустим 1000 рублям соответсвует 2 доллара
        course_one_value = 2 * currency_one.multiplicity / 100
        Course.objects.get_or_create(currency=currency_one, course=course_one_value)

        # Допустим 100 рублям соответсвует 15 евро
        currency_two_value = 15 * currency_two.multiplicity / 100
        Course.objects.get_or_create(currency=currency_two, course=currency_two_value)

        User.objects.all().delete()

        User.objects.create_superuser('superuser@mail.ru', 'password', balance=1000, currency=currency_base)
        User.objects.create_user('user_one@mail.ru', 'password', balance=1000, currency=currency_one)
        User.objects.create_user('user_two@mail.ru', 'password', balance=1000, currency=currency_two)
