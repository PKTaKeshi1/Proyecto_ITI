from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.cobranza_model import CobranzaModel
from models.factura_model import FacturaModel
from models.venta_model import VentaModel
from models.cliente_model import ClienteModel
from datetime import datetime

cobranza_bp = Blueprint('cobranza', __name__)
cobranza_model = CobranzaModel()
factura_model = FacturaModel()
venta_model = VentaModel()
cliente_model = ClienteModel()

@cobranza_bp.route('/cobranza/registrar/<int:id_factura>', methods=['GET', 'POST'])
def registrar_cobranza(id_factura):
    try:
        factura = factura_model.obtener_factura_por_id(id_factura)
        if not factura:
            flash("Factura no encontrada.", "danger")
            return redirect(url_for('factura.listar'))

        cliente = cliente_model.obtener_cliente_por_id(factura[13])  # ✅ id_cliente en la posición 13
        if not cliente:
            flash("Cliente no encontrado.", "danger")
            return redirect(url_for('factura.listar'))

        monto_total = float(factura[6])  # ✅ monto_total (posición 6)
        monto_pagado = cobranza_model.obtener_total_pagado(id_factura)
        monto_restante = round(monto_total - monto_pagado, 2)

        if request.method == 'POST':
            monto_pago_raw = request.form['monto_pago']

            try:
                monto_pago = float(monto_pago_raw)
            except ValueError:
                flash("El monto ingresado no es válido. Debe ser un número.", "warning")
                return redirect(request.url)

            if monto_pago <= 0:
                flash("El monto debe ser mayor que cero.", "warning")
                return redirect(request.url)

            if monto_pago > monto_restante:
                flash(f"El monto excede el saldo pendiente. Monto restante: {monto_restante:.2f}", "warning")
                return redirect(request.url)

            id_usuario = session.get('usuario_id')
            fecha_pago = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            id_cliente = factura[13]  # ✅

            cobranza_model.registrar_cobranza(id_factura, id_cliente, monto_pago, fecha_pago, id_usuario)
            flash("Cobranza registrada correctamente.", "success")
            return redirect(url_for('factura.listar'))

        return render_template(
            'cobranza/registrar.html',
            factura=factura,
            cliente=cliente,
            monto_pagado=monto_pagado,
            monto_restante=monto_restante
        )

    except Exception as e:
        flash(f"Error al registrar la cobranza: {str(e)}", 'danger')
        return redirect(url_for('factura.listar'))

@cobranza_bp.route('/cobranzas')
def listar_cobranzas():
    try:
        cobranzas = cobranza_model.listar_cobranzas()
        return render_template('cobranza/listar.html', cobranzas=cobranzas)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('factura.listar'))
