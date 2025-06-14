# Кредитная История

Современное веб-приложение на Flask для управления и мониторинга кредитной истории.

## Основные возможности

- Регистрация с указанием полных персональных данных
- Удобный личный кабинет с дашбордом кредитов
- Отслеживание статуса и сроков платежей
- История всех платежей по кредитам
- Анализ кредитной нагрузки

## Требования

- Python 3.8 или выше
- Зависимости из файла requirements.txt

## Установка и запуск

1. Клонируйте репозиторий или распакуйте архив с проектом
2. Перейдите в директорию проекта

```bash
cd путь_к_проекту
```

3. Создайте и активируйте виртуальное окружение (опционально, но рекомендуется)

```bash
python -m venv venv
```

Для Windows:
```bash
venv\Scripts\activate
```

Для Linux/Mac:
```bash
source venv/bin/activate
```

4. Установите зависимости

```bash
pip install -r requirements.txt
```

5. Инициализируйте базу данных

```bash
flask --app app init-db
```

6. Запустите приложение

```bash
python app.py
```

7. Откройте браузер и перейдите по адресу http://127.0.0.1:5000

## Демонстрационные учетные записи

Для демонстрации в системе созданы два пользователя:

1. **Иванов Иван Петрович**
   - Логин: `ivanov`
   - Пароль: `password1`
   - Email: ivanov@example.com
   - Кредиты: 1 активный кредит в Сбербанке

2. **Петрова Елена Сергеевна**
   - Логин: `petrova`
   - Пароль: `password2`
   - Email: petrova@example.com
   - Кредиты: 2 активных кредита (ВТБ и Альфа-Банк)

## Структура проекта

- `app/` - основной пакет приложения
  - `__init__.py` - инициализация приложения
  - `auth.py` - маршруты аутентификации
  - `credit.py` - маршруты для работы с кредитной историей
  - `db.py` - функции для работы с базой данных
  - `models.py` - модели данных
  - `schema.sql` - схема базы данных
  - `static/` - статические файлы (CSS, JS)
  - `templates/` - шаблоны HTML
- `instance/` - директория для базы данных
- `app.py` - точка входа в приложение
- `requirements.txt` - зависимости проекта
