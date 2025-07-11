from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import db, Utilizator
from datetime import date

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Utilizator.query.filter_by(Nume_Utilizator=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Te-ai autentificat cu succes, {user.Nume_Utilizator}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Autentificare eșuată. Nume de utilizator sau parolă incorecte.', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user_exists = Utilizator.query.filter((Utilizator.Nume_Utilizator == username) | (Utilizator.Email == email)).first()
        if user_exists:
            flash('Numele de utilizator sau adresa de email există deja.', 'danger')
        else:
            new_user = Utilizator(Nume_Utilizator=username, Email=email, Data_Creare=date.today())
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Contul a fost creat cu succes! Te poți autentifica acum.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ai fost deconectat.', 'info')
    return redirect(url_for('main.index'))
