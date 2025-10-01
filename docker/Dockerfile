# Используем полный образ Debian с Python
FROM python:3.11-bullseye

# Рабочая директория
WORKDIR /app

# Устанавливаем русскую локаль
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y locales \
    && echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen ru_RU.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Переменные окружения для русской локали
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

# Открываем порт
EXPOSE 5001

# Запуск приложения
CMD ["python", "app.py"]
