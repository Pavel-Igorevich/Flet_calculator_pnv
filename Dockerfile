FROM python:3.12-alpine

WORKDIR /app

# Копируем файл requirements.txt в текущую директорию образа
COPY requirements.txt .

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install -r requirements.txt

# Копируем все остальные файлы приложения в текущую директорию образа
COPY . .

# Копируем файл конфигурации NGINX внутрь контейнера
COPY nginx.conf /etc/nginx/nginx.conf

# Определяем точку входа и команду по умолчанию
ENTRYPOINT [ "python" ]
CMD ["main.py"]

# Expose the port your app runs on
EXPOSE 80