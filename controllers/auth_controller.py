from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.auth_model import AuthModel
from exceptions.autenticacion_excepcion import AutenticacionException

auth_bp = Blueprint('auth_bp', __name__, template_folder='../view/auth')

modelo = AuthModel()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        try:
            usuario_data = modelo.validar_usuario(usuario, contraseña)
            session['usuario'] = usuario_data['usuario']
            session['usuario_id'] = usuario_data['id_usuario']
            return redirect(url_for('usuario.menu'))  # Redirige al módulo de usuarios
        except AutenticacionException as e:
            flash(e.mensaje, 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))
