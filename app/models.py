from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

class User(UserMixin):
    def __init__(self, id, username, password, inn=None, pdf_path=None, verification_status=None):
        self.id = id
        self.username = username
        self.password = password
        self.inn = inn
        self.pdf_path = pdf_path
        self.verification_status = verification_status

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
        if user is None:
            return None
            
        return User(
            id=user['id'],
            username=user['username'],
            password=user['password'],
            inn=user['inn'],
            pdf_path=user['pdf_path'],
            verification_status=user['verification_status']
        )
    
    @staticmethod
    def get_by_username(username):
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            return None
            
        return User(
            id=user['id'],
            username=user['username'],
            password=user['password'],
            inn=user['inn'],
            pdf_path=user['pdf_path'],
            verification_status=user['verification_status']
        )
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def update_inn(self, inn):
        db = get_db()
        db.execute(
            'UPDATE user SET inn = ?, verification_status = ? WHERE id = ?',
            (inn, 'Ожидание...', self.id)
        )
        db.commit()
        self.inn = inn
        self.verification_status = 'Ожидание...'
    
    def update_pdf(self, pdf_path):
        db = get_db()
        db.execute(
            'UPDATE user SET pdf_path = ? WHERE id = ?',
            (pdf_path, self.id)
        )
        db.commit()
        self.pdf_path = pdf_path
    
    def update_verification_status(self, status):
        db = get_db()
        db.execute(
            'UPDATE user SET verification_status = ? WHERE id = ?',
            (status, self.id)
        )
        db.commit()
        self.verification_status = status

class Credit:
    def __init__(self, id, user_id, amount, date, status, bank, interest_rate=None, 
                 term=None, monthly_payment=None, next_payment_date=None, 
                 remaining_amount=None, overdue_amount=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.date = date
        self.status = status
        self.bank = bank
        self.interest_rate = interest_rate
        self.term = term
        self.monthly_payment = monthly_payment
        self.next_payment_date = next_payment_date
        self.remaining_amount = remaining_amount
        self.overdue_amount = overdue_amount or 0
        self.payments = []
    
    @staticmethod
    def get_by_user_id(user_id):
        db = get_db()
        credits = db.execute(
            'SELECT * FROM credit WHERE user_id = ?', (user_id,)
        ).fetchall()
        
        result = []
        for row in credits:
            credit = Credit(
                id=row['id'],
                user_id=row['user_id'],
                amount=row['amount'],
                date=row['date'],
                status=row['status'],
                bank=row['bank'],
                interest_rate=row['interest_rate'],
                term=row['term'],
                monthly_payment=row['monthly_payment'],
                next_payment_date=row['next_payment_date'],
                remaining_amount=row['remaining_amount'],
                overdue_amount=row['overdue_amount']
            )
            
            # Получаем историю платежей для кредита
            payments = db.execute(
                'SELECT * FROM payment WHERE credit_id = ? ORDER BY date DESC', 
                (credit.id,)
            ).fetchall()
            
            credit.payments = [
                Payment(
                    id=p['id'],
                    credit_id=p['credit_id'],
                    amount=p['amount'],
                    date=p['date'],
                    status=p['status']
                )
                for p in payments
            ]
            
            result.append(credit)
        
        return result

class Payment:
    def __init__(self, id, credit_id, amount, date, status):
        self.id = id
        self.credit_id = credit_id
        self.amount = amount
        self.date = date
        self.status = status
    
    @staticmethod
    def add_payment(credit_id, amount, date, status):
        db = get_db()
        db.execute(
            'INSERT INTO payment (credit_id, amount, date, status) VALUES (?, ?, ?, ?)',
            (credit_id, amount, date, status)
        )
        db.commit()
