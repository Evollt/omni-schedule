# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем русскую локаль
RUN apt-get update && apt-get install -y locales \
    && locale-gen ru_RU.UTF-8 \
    && update-locale LANG=ru_RU.UTF-8
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8

# Копируем зависимости
COPY requirements.txt .

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt \
    --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# Открываем порт, на котором работает Flask
EXPOSE 5001

# Запускаем приложение
CMD ["python", "app.py"]
