import os
import shutil

# Создаем папку app, если она еще не существует
os.makedirs('app', exist_ok=True)

# Список директорий и файлов, которые нужно скопировать
directories = [
    "assets",
    "calculations",
    "banner",
    "canvas",
    "construction",
    "orders",
    "plastic",
    "press_wall",
    "sheet_materials",
]

# Копируем выбранные директории и файлы в папку app
for item in directories:
    shutil.copytree(item, os.path.join('app', item))

# Копируем выбранные файлы в папку app
files = [
    "requirements.txt",
    "data.json",
    "data.py",
    "Dockerfile",
    "list_orders.py",
    "main.py",
    "nginx.conf",
    "other_func.py",
    "results_other_func.py",
    "theme.py"
]

for item in files:
    shutil.copy(item, 'app')

print("Копирование завершено.")