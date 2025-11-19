# app/routes/usuarios_routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import mysql
import pymysql
from app.utils.decorators import roles_required

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios')
@login_required
@roles_required(['admin'])
def lista_usuarios():
    cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE activo = 1")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template("usuarios/lista.html", usuarios=usuarios)

@usuarios_bp.route('/usuarios/agregar', methods=['GET', 'POST'])
@login_required
@roles_required(['admin'])
def agregar_usuario():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO usuarios (username, email, password, role) VALUES (%s, %s, %s, %s)',
            (username, email, password, role)
        )
        mysql.connection.commit()
        cursor.close()
        flash('Usuario agregado correctamente')
        return redirect(url_for('usuarios.lista_usuarios'))
    return render_template('usuarios/formulario.html', accion='Agregar', usuario={})


@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin'])
def editar_usuario(id):
    cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        cursor.execute(
            'UPDATE usuarios SET username=%s, email=%s, role=%s WHERE id=%s',
            (username, email, role, id)
        )
        mysql.connection.commit()
        flash('Usuario actualizado')
        return redirect(url_for('usuarios.lista_usuarios'))
    cursor.execute('SELECT id, username, email, role FROM usuarios WHERE id=%s', (id,))
    usuario = cursor.fetchone()
    cursor.close()
    return render_template('usuarios/formulario.html', accion='Editar', usuario=usuario)

@usuarios_bp.route('/usuarios/desactivar/<int:id>')
@login_required
@roles_required(['admin'])
def desactivar_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash("Usuario desactivado correctamente", "warning")
    return redirect(url_for("usuarios.lista_usuarios"))

@usuarios_bp.route('/usuarios/inactivos')
@login_required
@roles_required(['admin'])
def usuarios_inactivos():
    cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE activo = 0")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template("usuarios/inactivos.html", usuarios=usuarios)

@usuarios_bp.route('/usuarios/reactivar/<int:id>')
@login_required
@roles_required(['admin'])
def reactivar_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET activo = 1 WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash("Usuario reactivado correctamente", "success")
    return redirect(url_for("usuarios.usuarios_inactivos"))
