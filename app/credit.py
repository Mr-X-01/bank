import os
import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from .models import Credit
from .db import get_db

bp = Blueprint('credit', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'pdf'

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('credit.dashboard'))
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    credits = []
    if current_user.verification_status == 'Проверен':
        credits = Credit.get_by_user_id(current_user.id)
    
    return render_template('credit/dashboard.html', credits=credits)

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    if request.method == 'POST':
        inn = request.form['inn']
        error = None

        if not inn:
            error = 'ИНН обязателен.'
        elif len(inn) != 12 and len(inn) != 10:
            error = 'ИНН должен содержать 10 или 12 цифр.'
        
        if 'pdf_file' not in request.files:
            if not current_user.pdf_path:
                error = 'PDF-файл обязателен.'
        else:
            file = request.files['pdf_file']
            if file.filename == '':
                if not current_user.pdf_path:
                    error = 'Не выбран файл.'
            elif not allowed_file(file.filename):
                error = 'Разрешены только PDF-файлы.'
            else:
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{current_user.id}_{filename}")
                file.save(file_path)
                current_user.update_pdf(file_path)
                flash('Файл успешно загружен.', 'success')

        if error is None:
            current_user.update_inn(inn)
            # Имитация процесса проверки
            # В реальном приложении здесь был бы асинхронный процесс
            time.sleep(1)  # Имитация задержки
            current_user.update_verification_status('Проверен')
            flash('Данные успешно обновлены.', 'success')
            return redirect(url_for('credit.dashboard'))

        flash(error, 'error')

    return render_template('credit/profile.html')
