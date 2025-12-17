FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY app ./app

# Директория для базы данных (будет подключаться том)
VOLUME ["/app/data"]

# Переменные окружения, чтобы db.py знал, где хранить базу
ENV DATA_DIR=/app/data
ENV DB_PATH=/app/data/todo.db

# Открываем порт контейнера
EXPOSE 80

# Команда запуска FastAPI через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
