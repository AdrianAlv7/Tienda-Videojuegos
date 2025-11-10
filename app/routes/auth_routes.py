from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin
from app import mysql
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)

# Clase de usuario para Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, username, password, role, activo FROM usuarios WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            if user['activo'] == 1 and check_password_hash(user['password'], password):
                login_user(User(user['id'], user['username'], user['role']))
                return redirect(url_for('main.index'))
            elif user['activo'] == 0:
                flash('Tu cuenta está inactiva. Contacta al administrador.', 'danger')
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('auth/login.html')


# LOGOUT
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # --- Puedes agregar más validaciones aquí ---
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM usuarios WHERE username = %s OR email = %s", (username, email))
        existe = cur.fetchone()
        if existe:
            flash('Ya existe un usuario con ese nombre o correo.')
            return render_template('auth/register.html')
        # Hash del password
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO usuarios (username, email, password, role) VALUES (%s, %s, %s, %s)",
                    (username, email, hashed_password, 'cliente'))
        mysql.connection.commit()
        cur.close()
        flash('Registro exitoso, ¡ahora inicia sesión!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')



