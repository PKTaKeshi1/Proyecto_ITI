from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.venta_model import VentaModel
from models.producto_model import ProductoModel
from models.cliente_model import ClienteModel
from models.vendedor_model import VendedorModel
from models.moneda_model import MonedaModel

venta_bp = Blueprint('venta', __name__)
venta_model = VentaModel()

@venta_bp.route('/ventas')
def listar_ventas():
    try:
        ventas = venta_model.listar_ventas()
        return render_template('ventas/listar.html', ventas=ventas)
    except Exception as e:
        flash(str(e), 'danger')
        return render_template('ventas/listar.html', ventas=[])

@venta_bp.route('/ventas/nueva')
def nueva_venta():
    try:
        productos = ProductoModel.listar_productos_activos()
        clientes = ClienteModel.listar_clientes_activos()
        vendedores = VendedorModel.listar_vendedores_activos()
        monedas = MonedaModel.listar_monedas_activas()
        return render_template(
            'ventas/crear.html',
            productos=productos,
            clientes=clientes,
            vendedores=vendedores,
            monedas=monedas
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('venta.listar_ventas'))

@venta_bp.route('/ventas/guardar', methods=['POST'])
def guardar_venta():
    try:
        id_cliente = request.form['id_cliente']
        id_vendedor = request.form['id_vendedor']
        id_moneda = request.form['id_moneda']
        id_usuario = session.get('usuario_id')  # valor por defecto si no hay sesión

        ids_producto = request.form.getlist('id_producto[]')
        cantidades = request.form.getlist('cantidad[]')
        precios_unitarios = request.form.getlist('precio_unitario[]')

        if not (ids_producto and cantidades and precios_unitarios):
            flash("Debe completar todos los campos de productos.", 'warning')
            return redirect(url_for('venta.nueva_venta'))

        detalles = []
        for i in range(len(ids_producto)):
            detalles.append({
                "id_producto": ids_producto[i],
                "cantidad": cantidades[i],
                "precio_unitario": precios_unitarios[i]
            })

        resultado = venta_model.registrar_venta(id_cliente, id_vendedor, id_usuario, detalles, id_moneda)

        flash(f"Venta registrada correctamente (ID: {resultado['id_venta']}, Total: {resultado['simbolo_moneda']} {resultado['total']:.2f})", "success")
        return redirect(url_for('venta.listar_ventas'))
    except Exception as e:
        flash(f"Error al registrar venta: {str(e)}", "danger")
        return redirect(url_for('venta.nueva_venta'))

@venta_bp.route('/ventas/detalle/<int:id_venta>')
def detalle_venta(id_venta):
    try:
        cabecera = venta_model.obtener_venta_por_id(id_venta)
        detalle = venta_model.obtener_detalle_venta(id_venta)
        return render_template('ventas/detalle.html', cabecera=cabecera, detalle=detalle)
    except Exception as e:
        flash(f"Error al obtener detalle de venta: {str(e)}", "danger")
        return redirect(url_for('venta.listar_ventas'))
