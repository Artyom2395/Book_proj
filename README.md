# Book_proj
# Django-приложение для управления книгами в библиотеке
Шаг 1: Установите Docker
Вы можете загрузить Docker для своей операционной системы с официального сайта Docker: https://docs.docker.com/get-docker/
Шаг 2: Клонируйте репозиторий
Склонируйте этот репозиторий с GitHub на ваш локальный компьютер:
```
git clone <URL репозитория>
``` 
Шаг 3: Перейдите в каталог проекта
Перейдите в каталог вашего проекта:
```
cd <название-каталога-проекта>
``` 
Шаг 4: Сборка Docker образов
В этом приложении есть два файла: Dockerfile для проекта, файл docker-compose.yaml для настройки проекта, выглядит так
```
version: '3'
services:
  redis:
    image: redis
    ports:
      - "6379:6379"
  mysql:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypassword
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
  django:
    build: .
    command: >
      sh -c "
        while ! mysqladmin ping -h 'mysql' --silent; do
          echo 'Waiting for mysql to become available...';
          sleep 1;
        done;
        echo 'MySQL is up and available' &&
        python manage.py migrate &&
        python manage.py runserver 0.0.0.0:8000
      "
    environment:
      - CELERY_BROKER_URL=redis://redis:6379
      - CELERY_RESULT_BACKEND=django-db
      - CELERY_CACHE_BACKEND=django-cache
      - DATABASE_HOST=mysql
      - DATABASE_NAME=mydatabase
      - DATABASE_USER=myuser
      - DATABASE_PASSWORD=mypassword
      - DATABASE_PORT=3306
      - DATABASE_ENGINE=mysql
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - mysql
  celery:
    build: .
    command: celery -A library_project worker -l INFO --pool=solo
    environment:
      - CELERY_BROKER_URL=redis://redis:6379
      - CELERY_RESULT_BACKEND=django-db
      - CELERY_CACHE_BACKEND=django-cache
    depends_on:
      - django
      - redis
    volumes:
      - .:/app

volumes:
  mysql_data:
```
Здесь у нас несколько сервисов: Redis, MySQL, Django и Celery.Пройдемся подробнеее по настройке каждого:
- Сервис Redis:
   - Берет образ Redis из Docker Hub.
   - Проксирует порт 6379, чтобы можно было получить доступ к Redis извне.

- Сервис MySQL:
   - Берет последнюю версию образа MySQL из Docker Hub.
   - Определяет переменные окружения для настройки базы данных:
     - MYSQL_ROOT_PASSWORD: пароль для суперпользователя MySQL.
     - MYSQL_DATABASE: имя базы данных.
     - MYSQL_USER: имя пользователя базы данных.
     - MYSQL_PASSWORD: пароль пользователя базы данных.
   - Проксирует порт 3306, чтобы можно было получить доступ к MySQL извне.
   - Создает том (volume) с именем "mysql_data" для сохранения данных MySQL в директории "/var/lib/mysql".

- Сервис Django:
   - Собирает образ для Django из текущего каталога (содержащего Dockerfile).
   - Запускает следующую команду:
     - Ожидает, пока сервер MySQL станет доступным.
     - Выполняет миграции базы данных Django.
     - Запускает сервер Django на порту 8000.
   - Определяет следующие переменные окружения:
     - CELERY_BROKER_URL: URL брокера Redis для Celery.
     - CELERY_RESULT_BACKEND: бэкэнд результата для Celery (используется база данных Django).
     - CELERY_CACHE_BACKEND: бэкэнд кэширования для Celery (используется кэш Django).
     - DATABASE_HOST: хост базы данных MySQL.
     - DATABASE_NAME: имя базы данных MySQL.
     - DATABASE_USER: имя пользователя MySQL.
     - DATABASE_PASSWORD: пароль пользователя MySQL.
     - DATABASE_PORT: порт MySQL.
     - DATABASE_ENGINE: движок базы данных MySQL.
   - Проксирует порт 8000, чтобы можно было получить доступ к серверу Django извне.
   - Зависит от сервисов Redis и MySQL.

- Сервис Celery:
   - Собирает образ для Celery из текущего каталога (содержащего Dockerfile).
   - Запускает следующую команду:
     - Запускает Celery воркер с указанными аргументами.
   - Определяет следующие переменные окружения:
     - CELERY_BROKER_URL: URL брокера Redis для Celery.
     - CELERY_RESULT_BACKEND: бэкэнд результата для Celery (используется база данных Django).
     - CELERY_CACHE_BACKEND: бэкэнд кэширования для Celery (используется кэш Django).
   - Зависит от сервисов Django и Redis.
   - Монтирует текущий каталог внутрь контейнера для доступа к исходному коду.

- Volumes:
   - Описывает том "mysql_data", который будет использоваться для сохранения данных MySQL.

Далее мы соберем Docker образы и запустим их. Убедитесь, что вы находитесь в каталоге вашего проекта и выполните следующую команду для сборки образов и запуска:
```
docker-compose up --build
``` 
Эта команда выполнит сборку образов на основе ваших Dockerfile файлов. Образы будут названы myproject_db для базы данных и myproject_web для вашего веб-сервиса.

Шаг 5: Проверка приложения
Тестируем работу приложения(н-р, Postman)
Отправляем post запрос на url http://127.0.0.1:8000/api/books/
в body > raw > втаявляем следующий запрос 
```
{
        "title": "Harry Potter 3",
        "author": "Joanne Rowling",
        "year_of_publication": 2006,
        "isbn": "458-318-3"
    }
```
Также можно пройти по всем запросам post, get, put, delete
Н-р, посморим один объект по id из БД, 
Отправляем get запрос на url http://127.0.0.1:8000/api/books/1/

Тестируем регистрацию,
Отправляем post запрос на url http://127.0.0.1:8000/api/users/register/
```
{
    "username": "User01",
    "email": "user01@gmail.com"
}
```
в ответ в консоль придет прветственное сообщение о том, что регистрация прошла успешно
Шаг 6: Завершение работы
Чтобы завершить работу приложения и остановить контейнеры, выполните следующую команду:

```
docker-compose down
```
Это остановит и удалит контейнеры.
