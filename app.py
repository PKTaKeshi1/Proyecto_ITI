from flask import Flask, render_template
from controllers.usuario_controller import usuario_bp
from controllers.factura_controller import factura_bp
from controllers.producto_controller import producto_bp
from controllers.vendedor_controller import vendedor_bp
from controllers.cliente_controller import cliente_bp
from controllers.auth_controller import auth_bp
from controllers.venta_controller import venta_bp
from controllers.cobranza_controller import cobranza_bp

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura_123'

# Registro de Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(factura_bp)
app.register_blueprint(producto_bp, url_prefix='/producto')
app.register_blueprint(vendedor_bp, url_prefix='/vendedor')
app.register_blueprint(cliente_bp, url_prefix='/cliente')
app.register_blueprint(venta_bp, url_prefix='/venta')
app.register_blueprint(cobranza_bp, url_prefix='/cobranza')
@app.route('/')
def index():
    return render_template("auth/login.html")       

if __name__ == '__main__':
    app.run(debug=True)
