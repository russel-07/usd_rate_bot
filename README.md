![workflow](https://github.com/russel-07/usd_rate_bot/actions/workflows/usd_rate_bot_workflow.yml/badge.svg)

# [USD RATE BOT](https://t.me/usd_rate_russel_bot/)
 
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![Gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

# Описание
[Usd Rate Bot](https://t.me/usd_rate_russel_bot/) - это телеграм-бот, в котором пользователь может узнать курс доллара на текущий момент, а также подписаться на периодическое получение курса доллара. Бот помнит и хранит историю получения курса для каждого пользователя и дает возможность в любой момент просмотреть историю своих запросов. Курс доллара обновляется ежедневно с понедельника по пятницу в 10:00. В это же время осуществляется рассылка с оповещением о новом курсе доллара для пользователей, подписанных на данную опцию.

## Функциональность проекта
- Регистрация нового пользователя из бота;
- Получение текущего курса доллара;
- Получение истории запросов пользователя;
- Получение данных о пользователе;
- Подписка/отписка пользователя на периодическое оповещение о новом курсе доллара;
- Получение ботом текстов для выдачи пользователю;
- Панель администрирования.

## Инфраструктура
- Проект написан на Python c использованием фреймворков Django, DRF, aiogram;
- В качестве wsgi-сервера используется Gunicorn;
- В качестве веб-сервера используется Nginx;
- В качестве СУБД используется PostgreSQL;
- Проект развернут и запущен на удаленном сервере Yandex.Cloud в Docker-контейнерах.

## Методы API
Все методы API доступны только администратору.  
  
- /user/<telegram_id>
    - GET - в ответ на запрос приходят данные о пользователе;
    - POST - создается новый пользователь;
    - PATCH - статус подписки пользователя на периодическое оповещене меняет свое состояние.
  
- /user/<telegram_id>/requests
    - GET - в ответ на запрос приходит история запросов пользователя о курсе доллара;
    - POST - в истории запросов пользователя сохраняется новая запись.

- /rate  
    - GET - в ответ на запрос приходит текущий курс доллара и сохраняется в кэше до следующего обновления курса.

- /notified_list  
    - GET - в ответ на запрос приходит список telegram_id пользователей, которые подписаны на периодическое оповещение о курсе доллара.
    
- /template_text/<slug>  
    - GET - в ответ на запрос приходит запрошенный шаблон текста:
        - /template_text/greeting - шаблон приветствия;
        - /template_text/rate - шаблон текущего курса доллара;
        - /template_text/user_data - шаблон данных пользователя;
        - /template_text/user_requests - шаблон истории запросов пользователя.
