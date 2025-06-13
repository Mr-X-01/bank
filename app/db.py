import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    # Добавляем демонстрационных пользователей
    db.execute(
        'INSERT INTO user (username, password, first_name, last_name, middle_name, email) VALUES (?, ?, ?, ?, ?, ?)',
        ('ivanov', generate_password_hash('password1'), 'Иван', 'Иванов', 'Петрович', 'ivanov@example.com')
    )
    db.execute(
        'INSERT INTO user (username, password, first_name, last_name, middle_name, email) VALUES (?, ?, ?, ?, ?, ?)',
        ('petrova', generate_password_hash('password2'), 'Елена', 'Петрова', 'Сергеевна', 'petrova@example.com')
    )
    
    # Добавляем тестовые кредиты для Иванова Ивана Петровича
    db.execute(
        'INSERT INTO credit (user_id, amount, date, status, bank, interest_rate, term, monthly_payment, next_payment_date, remaining_amount, overdue_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (1, 100000, '2025-01-15', 'Активный', 'Сбербанк', 12.5, 24, 4700.85, '2025-07-15', 56410.20, 0)
    )
    
    # Добавляем платежи для первого кредита
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (1, 4700.85, '2025-02-15', 'Оплачен')
    )
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (1, 4700.85, '2025-03-15', 'Оплачен')
    )
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (1, 4700.85, '2025-04-15', 'Оплачен')
    )
    
    # Добавляем тестовые кредиты для Петровой Елены Сергеевны
    db.execute(
        'INSERT INTO credit (user_id, amount, date, status, bank, interest_rate, term, monthly_payment, next_payment_date, remaining_amount, overdue_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (2, 50000, '2025-02-20', 'Активный', 'ВТБ', 10.9, 12, 4416.67, '2025-06-20', 13250.01, 4416.67)
    )
    db.execute(
        'INSERT INTO credit (user_id, amount, date, status, bank, interest_rate, term, monthly_payment, next_payment_date, remaining_amount, overdue_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (2, 75000, '2025-05-10', 'Активный', 'Альфа-Банк', 11.5, 36, 2475.82, '2025-07-10', 49516.40, 0)
    )
    
    # Добавляем платежи для второго кредита
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (2, 4416.67, '2025-03-20', 'Оплачен')
    )
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (2, 4416.67, '2025-04-20', 'Оплачен')
    )
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (2, 4416.67, '2025-05-20', 'Просрочен')
    )
    
    # Добавляем платежи для третьего кредита
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (3, 2475.82, '2025-06-10', 'Оплачен')
    )
    db.execute(
        'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
        (3, 2475.82, '2025-07-10', 'Оплачен')
    )
    
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Очистить существующие данные и создать новые таблицы."""
    init_db()
    click.echo('База данных инициализирована.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
