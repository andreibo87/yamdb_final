![Python version](https://img.shields.io/badge/python-3.7-yellow) 
![Django version](https://img.shields.io/badge/django-2.2-orange) 
![workflow status](https://github.com/andreibo87/yamdb_final/actions/workflows/main.yml/badge.svg)

#  Проект YaMDb
Проект Yambd - база отзывов о произведениях искусства и не только. Версия V1.

Проект доступен по адресу : http://51.250.101.169/admin

##### Особенности данной версии
→ Доступна для рецензий база данных произведений из трех категорий : «Книги», «Фильмы», «Музыка». 
→ Возможность оценки произведения от 1 до 10 баллов.
→ Возможность комментирования чужих рецензий.
→ Аутентификация пользователей по JWT-токену 
→ Настройки прав доступа пользователей ( Суперадминистратор, Администратор, Модератор, Пользователь).

### Технологии
Python 3.7, Django 3.2, DRF, NGINX, Gunicorn, Docker

### Запуск проекта
- Клонируйте репозиторий на ваше рабочее устройство 
```
git@github.com:andreibo87/yamdb_final.git
```
- Создайте файл переменного окружения и заполните его по аналогии с примером .env.example
```
cd infra
nano .env
```
- Перейдите в директорию с инструкциями по запуску контейнеров 
```
cd infra
```
- Запустите сборку контейнеров
```
sudo docker-compose up
```
- Выполните миграции, создайте суперпользователя и соберите статику
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
- Заполните базу данных тестовыми данными
```
Пройдите по адресу http://localhost/admin/ , авторизуйтесь как созданный выше суперпользователь,
и внесите записи в базу данных через админ панель.
```

### Техподдержка
##### Если у вас что либо не работает, пожалуйста, перезагрузите ваш компьютер, ноутбук или смартфон.
Если и это не поможет, просьба обратиться к создателю проекта:
- Telegram : @andreibo87
- Telegram-bot : @YamdbBotHelper
