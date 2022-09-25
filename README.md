# Yatube - социальная сеть для блогеров

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

## Описание проекта

Проект создан в рамках учебного курса Яндекс.Практикум.

Социальная сеть для авторов и подписчиков. Пользователи могут подписываться на избранных авторов, оставлять и удалять комментари к постам, оставлять новые посты на главной странице и в тематических группах, прикреплять изображения к публикуемым постам.

Проект реализован на MVT-архитектуре, реализована система регистрации новых пользователей, восстановление паролей пользователей через почту, система тестирования проекта на unittest, пагинация постов и кэширование страниц. Проект имеет верстку с адаптацией под размер экрана устройства пользователя.

## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/IvanMaximov/yatube.git
cd yatube
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv env
```

```bash
source env/bin/activate
```

* Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

* Выполните миграции:

```bash
cd yatube
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```
