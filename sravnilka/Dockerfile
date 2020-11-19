# Загружаем официальный образ
FROM python:3.8.3-alpine

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей
RUN pip install --upgrade pip

RUN apk update \
    && apk add libxml2-dev libxslt-dev postgresql-dev python3-dev gcc libc-dev jpeg-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Копируем проект
COPY . .