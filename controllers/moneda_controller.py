from flask import Blueprint, render_template, request, redirect, url_for
from models.moneda_model import MonedaModel

moneda_bp = Blueprint('moneda_bp', __name__, template_folder='../view/moneda')

modelo = MonedaModel()

@moneda_bp.route('/monedas')
def listar_monedas():
    monedas = modelo.listar_monedas()
    return render_template('listar.html', monedas=monedas)

@moneda_bp.route('/monedas/crear', methods=['GET', 'POST'])
def crear_moneda():
    if request.method == 'POST':
        modelo.crear_moneda(
            request.form['id_moneda'],
            request.form['nombre_moneda'],
            request.form['simbolo'],
            request.form['cambio_actual'],
            request.form['fecha_actualizacion'],
            request.form['subunidad']
        )
        return redirect(url_for('moneda_bp.listar_monedas'))
    return render_template('formulario.html')
