from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .banco import session
from werkzeug.security import generate_password_hash, check_password_hash
import logging
logger = logging.getLogger(__name__)

# Roteamento mínimo (adapte se usar blueprints)
from flask import current_app as app

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # mostra últimos 20 registros
    consultas = session.query(User).all()  # ajuste para consultas
    from .models import Consulta
    consultas = session.query(Consulta).order_by(Consulta.data.desc()).limit(20).all()
    return render_template('dashboard.html', consultas=consultas)

# utilitário para criar admin (execute uma vez via console)
def create_admin(username, password):
    existing = session.query(User).filter_by(username=username).first()
    if existing:
        logger.info("Usuário já existe")
        return existing
    u = User(username=username, password=generate_password_hash(password))
    session.add(u)
    session.commit()
    logger.info("Admin criado: %s", username)
    return u
