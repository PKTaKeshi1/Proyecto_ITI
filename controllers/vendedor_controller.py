from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.vendedor_model import VendedorModel

vendedor_bp = Blueprint('vendedor', __name__, url_prefix='/vendedor')

@vendedor_bp.route('/listar')
def listar():
    vendedores = VendedorModel.listar_vendedores()
    return render_template('vendedor/listar.html', vendedores=vendedores)

@vendedor_bp.route('/crear')
def crear():
    return render_template('vendedor/crear.html')

@vendedor_bp.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    celular = request.form['celular']
    correo = request.form['correo']
    id_usuario = session.get('usuario_id')
    if id_usuario is None:
        return redirect(url_for('auth_bp.login'))

    VendedorModel.insertar_vendedor(nombre, apellido, celular, correo, id_usuario)
    flash('✅ Vendedor registrado correctamente.', 'success')
    return redirect(url_for('vendedor.listar'))

@vendedor_bp.route('/editar/<int:id_vendedor>')
def editar(id_vendedor):
    vendedor = VendedorModel.obtener_por_id(id_vendedor)
    return render_template('vendedor/editar.html', vendedor=vendedor)

@vendedor_bp.route('/actualizar/<int:id_vendedor>', methods=['POST'])
def actualizar(id_vendedor):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    celular = request.form['celular']
    correo = request.form['correo']
    VendedorModel.actualizar_vendedor(id_vendedor, nombre, apellido, celular, correo)
    flash('✅ Vendedor actualizado correctamente.', 'success')
    return redirect(url_for('vendedor.listar'))

@vendedor_bp.route('/eliminar/<int:id_vendedor>')
def eliminar(id_vendedor):
    VendedorModel.eliminar_vendedor(id_vendedor)
    flash('🗑️ Vendedor eliminado correctamente.', 'warning')
    return redirect(url_for('vendedor.listar'))
