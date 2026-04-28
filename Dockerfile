# Используем компактный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем библиотеку
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт
COPY main.py .

# Запуск скрипта при старте контейнера
CMD ["python", "main.py"]
