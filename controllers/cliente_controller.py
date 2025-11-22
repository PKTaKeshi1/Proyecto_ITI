from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.cliente_model import ClienteModel

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

# Listar
@cliente_bp.route('/listar')
def listar():
    clientes = ClienteModel.listar_clientes()
    return render_template('cliente/listar.html', clientes=clientes)

# Crear
@cliente_bp.route('/crear')
def crear():
    return render_template('cliente/crear.html')

# Guardar
@cliente_bp.route('/guardar', methods=['POST'])
def guardar():
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    razon_social = request.form['razon_social']
    tipo_doc = request.form['tipo_doc']
    dni_ruc = request.form['dni_ruc'].strip()
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']
    id_usuario = session.get('usuario_id')

    # Validación del tipo de documento
    if tipo_doc == 'DNI' and len(dni_ruc) != 8:
        flash('El DNI debe tener exactamente 8 dígitos.', 'danger')
        return redirect(url_for('cliente.crear'))
    if tipo_doc == 'RUC' and len(dni_ruc) != 11:
        flash('El RUC debe tener exactamente 11 dígitos.', 'danger')
        return redirect(url_for('cliente.crear'))

    if id_usuario is None:
        return redirect(url_for('auth_bp.login'))

    ClienteModel.insertar_cliente(
        nombres, apellidos, razon_social, tipo_doc,
        dni_ruc, direccion, telefono, email, id_usuario
    )
    flash('Cliente registrado correctamente.', 'success')
    return redirect(url_for('cliente.listar'))

# Editar
@cliente_bp.route('/editar/<int:id_cliente>')
def editar(id_cliente):
    cliente = ClienteModel.obtener_cliente_por_id(id_cliente)
    return render_template('cliente/editar.html', cliente=cliente)

# Actualizar
@cliente_bp.route('/actualizar/<int:id_cliente>', methods=['POST'])
def actualizar(id_cliente):
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    razon_social = request.form['razon_social']
    tipo_doc = request.form['tipo_doc']
    dni_ruc = request.form['dni_ruc'].strip()
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']

    if tipo_doc == 'DNI' and len(dni_ruc) != 8:
        flash('El DNI debe tener exactamente 8 dígitos.', 'danger')
        return redirect(url_for('cliente.editar', id_cliente=id_cliente))
    if tipo_doc == 'RUC' and len(dni_ruc) != 11:
        flash('El RUC debe tener exactamente 11 dígitos.', 'danger')
        return redirect(url_for('cliente.editar', id_cliente=id_cliente))

    ClienteModel.actualizar_cliente(
        id_cliente, nombres, apellidos, razon_social,
        tipo_doc, dni_ruc, direccion, telefono, email
    )
    flash('Cliente actualizado correctamente.', 'success')
    return redirect(url_for('cliente.listar'))

# Eliminar
@cliente_bp.route('/eliminar/<int:id_cliente>')
def eliminar(id_cliente):
    ClienteModel.eliminar_cliente(id_cliente)
    flash('Cliente eliminado correctamente.', 'warning')
    return redirect(url_for('cliente.listar'))
