# Используем python 3.11.2 базовый образ
FROM python:3.11.2

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Установка клиента MySQL
RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && rm -rf /var/lib/apt/lists/*
# Копируем зависимости проекта в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущей директории в контейнер
COPY . /app

# Команда для запуска celery
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
