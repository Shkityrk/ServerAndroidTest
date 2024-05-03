FROM python:3.11
EXPOSE 8000
# Устанавливаем переменную окружения для запуска в неинтерактивном режиме
ENV PYTHONUNBUFFERED 1


# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости Python из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое текущей директории в контейнер в директорию /app/
COPY . /app/


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]