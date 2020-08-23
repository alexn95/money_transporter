from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from datetime import datetime


class Currency(models.Model):
    symbol = models.CharField(max_length=10, verbose_name='Символ', unique=True)
    title = models.CharField(max_length=50, verbose_name='Название', unique=True)
    multiplicity = models.SmallIntegerField(verbose_name='Кратность')
    is_base = models.BooleanField(default=False, verbose_name='Эта валюта базовая')

    @property
    def actual_course(self):
        """Получение последнего акуального курса валюты"""
        return self.courses.filter(start_datetime__lt=datetime.now()).order_by('-start_datetime').first()

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.title


class Course(models.Model):
    start_datetime = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Дата и время начала действия курса'
    )
    course = models.FloatField(verbose_name='Курс')
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE,
        related_name='courses', verbose_name='Валюта'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        get_latest_by = 'start_datetime'

    def __str__(self):
        return self.currency.title


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email необходимо задать')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True,
        verbose_name='Валюта'
    )
    balance = models.FloatField(default=0, verbose_name='Баланс счета')

    is_staff = models.BooleanField('Это персонал', default=False)

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = UserManager()

    def __str__(self):
        return self.email


class Transaction(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='send_transactions',
        verbose_name='Отправитель',
    )
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='receive_transactions',
        verbose_name='Получатель'
    )

    sender_amount = models.FloatField(verbose_name='Сумма перевода в валюте отправителя')
    recipient_amount = models.FloatField(verbose_name='Сумма перевода в валюте получателя')

    sender_currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True,
        related_name='send_transactions',
        verbose_name='Валюта отправителя'
    )
    recipient_currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True,
        related_name='receive_transactions',
        verbose_name='Валюта получателя'
    )

    create_datetime = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Дата и время совершаения транзакции'
    )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.sender} to {self.recipient}'
