# Тестовое задание Django + Stripe API
Проект взаимодействия фраемворка __Django__ и платёжной системы __Stripe__.

## Запуск проекта без Docker

1. ``Клонировать репозиторий https://github.com/OverDrive13/Stripe_task``
2. ``cd api_django_stripe/``
3. ``python -m venv venv``
4. ``source venv/Scripts/activate``
5. ``pip install -r requirements.txt``
6. ``Заполнить .env файл`` 

### Образец:
```
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY= 

STRIPE_PUBLIC_KEY= Ключи из https://stripe.com/docs
STRIPE_SECRET_KEY= После регистрации ключи будут на https://dashboard.stripe.com/test/apikeys

```
### База Данных
В репозитории уже есть db.sqlite3

``cd stripe``
``python manage.py runserver``
```

## Запуск с помощью Docker

Убедитесь, что вы находитесь в той же директории, где сохранён Dockerfile
``docker-compose up -d --build``

Проект доступен: ``localhost:8000``

***
``http://127.0.0.0:8000/`` - главная страница проекта

``http://127.0.0.1:8000/admin`` - административная панель с возможностью редактирования 

Для входа в админ панель воспользуйтесь логином admin и паролем admin
В админ панеле есть возможность просмотра модели Item и добавления новых.
