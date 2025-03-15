# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

COPY requirements.txt .
# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org


# Открываем порт, на котором работает Flask
EXPOSE 5001

# Запускаем приложение
CMD ["python", "app.py"]
