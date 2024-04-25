FROM python:3.12-alpine

WORKDIR /app

# Копируем файл requirements.txt в текущую директорию образа
COPY requirements.txt .

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install -r requirements.txt

# Копируем все остальные файлы приложения в текущую директорию образа
COPY . .

# Определяем точку входа и команду по умолчанию

ENTRYPOINT [ "flet" ]
CMD ["run", "--web", "main.py", "-p", "8000"]

# Expose the port your app runs on
EXPOSE 8000