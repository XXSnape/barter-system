# Бартер система на Django Rest Framework

## Проект выполнен в рамках тестового задания 

### API находится по адресу: http://localhost:8000/api/v1
### Регистрация пользователей возможна по адресу: http://localhost:8000/api/v1/auth/sign-up

### Фронтенд для создания объявлений находится по адресу: http://localhost:8000/ads

### Установка
1) Клонируйте репозиторий:
```sh
git clone https://github.com/XXSnape/barter-system.git
```

2) Создайте виртуальное окружение для python 3.12+ и установите зависимости:
```sh
pip install poetry
```
```sh
poetry install
```

3) Перейдите в директорию проекта src:
```sh
cd src
```

4) Выполните миграции базы данных:
```sh
python manage.py migrate
```

5) Запустите тесты:
```sh
python manage.py test
```

6) Запустите сервер:
```sh
python manage.py runserver
```
