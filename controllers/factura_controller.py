from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from models.factura_model import FacturaModel
from models.venta_model import VentaModel
from models.moneda_model import MonedaModel
from weasyprint import HTML
from num2words import num2words  # <--- LIBRERÍA PARA CONVERTIR A LETRAS

factura_bp = Blueprint('factura', __name__)
factura_model = FacturaModel()
venta_model = VentaModel()
moneda_model = MonedaModel()

@factura_bp.route('/factura/pdf/<int:id_factura>')
def generar_factura_pdf(id_factura):
    try:
        factura = factura_model.obtener_factura_por_id(id_factura)
        detalle = venta_model.obtener_detalle_venta(factura[7])  # factura[7] = id_venta

        if not factura or not detalle:
            flash("Factura o detalle no encontrado.", "danger")
            return redirect(url_for('factura.listar'))

        # Conversión del total a letras
        total = round(factura[6], 2)
        parte_entera = int(total)
        parte_decimal = int(round((total - parte_entera) * 100))
        letras = num2words(parte_entera, lang='es').title()
        monto_letras = f'{letras} con {parte_decimal:02d}/100 Soles'

        # ⬇️ AHORA YA NO SE GENERA PDF, SOLO SE MUESTRA UNA VISTA HTML
        return render_template(
            'factura/vista_factura.html',
            factura=factura,
            detalle=detalle,
            monto_letras=monto_letras
        )

    except Exception as e:
        flash(f"Error al mostrar factura: {str(e)}", "danger")
        return redirect(url_for('factura.listar'))

@factura_bp.route('/facturas')
def listar():
    try:
        facturas = factura_model.listar_facturas()
        return render_template('factura/listar.html', facturas=facturas)
    except Exception as e:
        flash(str(e), 'danger')
        return render_template('factura/listar.html', facturas=[])

@factura_bp.route('/menu-factura')
def menu_factura():
    return render_template('factura/menu.html')

@factura_bp.route('/factura/emitir/<int:id_venta>', methods=['GET', 'POST'])
def emitir(id_venta):
    try:
        venta = venta_model.obtener_venta_por_id(id_venta)
        if not venta:
            flash('La venta no existe.', 'warning')
            return redirect(url_for('factura.menu_factura'))

        ya_facturada = factura_model.existe_factura_para_venta(id_venta)

        if request.method == 'POST':
            if ya_facturada:
                flash('Esta venta ya tiene una factura emitida.', 'warning')
                return redirect(url_for('factura.menu_factura'))

            serie = request.form['serie'].strip().upper()
            numero = request.form['numero'].strip()
            id_moneda = int(request.form['id_moneda'])
            id_usuario = session.get('usuario_id')
            tipo_comprobante = 1  # fijo a factura

            # Verifica si ya existe una factura con esa serie y número
            if factura_model.existe_factura_por_serie_numero(serie, numero):
                flash('Ya existe una factura con esa serie y número.', 'danger')
                return redirect(request.url)

            factura_model.emitir_factura(id_venta, id_usuario, id_moneda, tipo_comprobante, serie, numero)

            flash('Factura emitida correctamente.', 'success')
            return redirect(url_for('factura.listar'))

        monedas = moneda_model.listar_monedas_activas()
        return render_template(
            'factura/emitir.html',
            venta=venta,
            monedas=monedas,
            ya_facturada=ya_facturada
        )

    except Exception as e:
        flash(f"Error al emitir la factura: {str(e)}", 'danger')
        return redirect(url_for('factura.menu_factura'))

