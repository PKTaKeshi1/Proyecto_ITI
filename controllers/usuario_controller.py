from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario_model import UsuarioModel
from datetime import datetime

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        modelo = UsuarioModel()
        user = modelo.verificar_credenciales(usuario, contraseña)
        if user:
            session['usuario_id'] = user['id_usuario']
            session['usuario_nombre'] = user['usuario']
            flash('Bienvenido, ' + user['nombres'], 'success')
            return redirect(url_for('usuario.menu'))
        else:
            flash('Usuario o contraseña incorrecta', 'danger')
    return render_template('auth/login.html')

@usuario_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        clave_admin = request.form['clave_admin']
        if len(usuario) < 5:
            flash("El nombre de usuario debe tener al menos 5 caracteres", "danger")
        elif len(contraseña) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "danger")
        elif clave_admin != "clave_secreta_admin":  
            flash("Clave secreta del admin incorrecta", "danger")
        else:
            hash_pass = generate_password_hash(contraseña)
            try:
                modelo = UsuarioModel()
                modelo.crear_usuario(
                    nombres=nombres,
                    apellidos=apellidos,
                    usuario=usuario,
                    contraseña=hash_pass,
                    usuario_creacion=usuario
                )
                flash("Usuario registrado correctamente", "success")
                return redirect(url_for('usuario.login'))
            except Exception as e:
                flash(str(e), "danger")
    return render_template("auth/registro.html")


@usuario_bp.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for('usuario.login'))

@usuario_bp.route('/menu')
def menu():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('usuario.login'))
    return render_template('menu.html')

