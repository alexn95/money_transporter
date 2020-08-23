# Переводчик денег (тестовое задание)

## Требования

Проект представляет из себя REST API, которое позволяет  выполнять следующие действия:
* зарегистрировать пользователя с указанием
   * начальный баланс
   * валюта счета
   * email (уникальный; используется для входа)
   * пароль
* аутентифицировать пользователя по почте и паролю
* перевести средства со своего счета на счет другого пользователя (используйте формулу конвертации, если валюты счетов отличаются)
* просмотреть список всех операций по своему счету
 

## Необходимо для запуска

* python3.7
* postgres

## Установка
1. Склонировать репозиторий 

```
$ git clone https://github.com/alexn95/money_transporter.git
$ cd money_transporter
```

2. Создать виртуальное оружение и активировать его

```
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Установить зависимостей

```
$ pip install -r requirements.txt
```

4. Создать settings_local.py на основе settings_local.py.template и соответствующую базу данных

5. Выполнить миграции

```
$ python manage.py migrate
```

6. Создать тестовые данные

```
$ python manage.py test_data
```

7. Запустить сервер

```
$ python manage.py runserver
```

Приложение доступно по http://127.0.0.1:8000/


## Запуск тестов

```
$ python manage.py test
``` 

### Рекомендации

По url http://127.0.0.1:8000/api/swagger/ доступна электронная документация к приложению, в которой можно найти
все доступные запросы.