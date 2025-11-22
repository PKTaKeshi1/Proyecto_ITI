from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.producto_model import ProductoModel

producto_bp = Blueprint('producto', __name__, url_prefix='/producto')

# Listar
@producto_bp.route('/listar')
def listar():
    productos = ProductoModel.listar_productos()
    return render_template('producto/listar.html', productos=productos)

# Crear
@producto_bp.route('/crear')
def crear():
    return render_template('producto/crear.html')

# Guardar
@producto_bp.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio_unitario = request.form['precio_unitario']
    stock = request.form['stock']
    id_usuario = session.get('usuario_id')  # ✅ CORREGIDO

    if id_usuario is None:
        return redirect(url_for('auth_bp.login'))

    ProductoModel.insertar_producto(nombre, descripcion, precio_unitario, stock, id_usuario)
    flash('✅ Producto registrado correctamente.', 'success')  # ✅ Toast: verde
    return redirect(url_for('producto.listar'))

# Editar
@producto_bp.route('/editar/<int:id_producto>')
def editar(id_producto):
    producto = ProductoModel.obtener_producto_por_id(id_producto)
    return render_template('producto/editar.html', producto=producto)

# Actualizar
@producto_bp.route('/actualizar/<int:id_producto>', methods=['POST'])
def actualizar(id_producto):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio_unitario = request.form['precio_unitario']
    stock = request.form['stock']
    ProductoModel.actualizar_producto(id_producto, nombre, descripcion, precio_unitario, stock)
    flash('✏️ Producto actualizado correctamente.', 'info')  # ✅ Toast: azul
    return redirect(url_for('producto.listar'))

# Eliminar
@producto_bp.route('/eliminar/<int:id_producto>')
def eliminar(id_producto):
    ProductoModel.eliminar_producto(id_producto)
    flash('🗑️ Producto eliminado correctamente.', 'warning')  # ✅ Toast: naranja
    return redirect(url_for('producto.listar'))
