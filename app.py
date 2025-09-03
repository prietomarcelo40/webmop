import os
from flask import Flask
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import logging

# ----------------------------
# Cargar variables de entorno
# ----------------------------
load_dotenv()

# ----------------------------
# Crear instancia de Flask
# ----------------------------
app = Flask(__name__, static_folder='static')

# ----------------------------
# Configuración de la app
# ----------------------------
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambiame_por_una_clave_segura')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_REMITENTE')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

# ----------------------------
# Inicializar extensiones
# ----------------------------
mail = Mail(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
csrf = CSRFProtect(app)

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# ----------------------------
# Importar y registrar Blueprint
# ----------------------------
# IMPORTANTE: después de crear app y extensiones
from rutas.web import web
app.register_blueprint(web)

# ----------------------------
# Ejecutar la app
# ----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"
    
    # HTTPS solo si estás en producción y tenés certificados
    # from flask_sslify import SSLify
    # sslify = SSLify(app)

    app.run(host='0.0.0.0', port=port, debug=debug_mode)
