import os
import logging
from flask import Flask, render_template, jsonify
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# ----------------------------
# Cargar variables de entorno
# ----------------------------
load_dotenv()

# ----------------------------
# Crear instancia de Flask
# ----------------------------
app = Flask(__name__, static_folder='static')

# ----------------------------
# Configuración de la app (desde variables de entorno)
# ----------------------------
# SECRET_KEY: OBLIGATORIA en producción. En desarrollo, usa un fallback seguro.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-cambiar-en-produccion')
if app.config['SECRET_KEY'] == 'dev-key-cambiar-en-produccion' and os.environ.get('RENDER_EXTERNAL_URL'):
    raise ValueError("SECRET_KEY no definida en producción. La aplicación no puede arrancar.")

# Configuración de sesiones seguras
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = bool(os.environ.get('RENDER_EXTERNAL_URL'))  # HTTPS en producción

# Configuración de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_REMITENTE')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

# Configuración de seguridad adicional
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = app.config['SECRET_KEY']

# Configuración de caché para archivos estáticos (1 año)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

# Variables para el botón de WhatsApp (desde variables de entorno)
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '5491133810134')
WHATSAPP_MESSAGE = os.environ.get('WHATSAPP_MESSAGE', 'Hola!%20Vi%20tu%20página%20y%20quiero%20más%20información.')
app.config['WHATSAPP_URL'] = f"https://wa.me/{WHATSAPP_NUMBER}?text={WHATSAPP_MESSAGE}"

# ----------------------------
# Inicializar extensiones
# ----------------------------
mail = Mail(app)
csrf = CSRFProtect(app)

# Rate Limiting: límites por IP. En producción, se recomienda usar Redis.
storage_uri = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=storage_uri
)

# ----------------------------
# Configuración de logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# ----------------------------
# Middleware de seguridad: cabeceras HTTP
# ----------------------------
@app.after_request
def security_headers(response):
    """
    Inyecta cabeceras de seguridad para prevenir ataques comunes.
    """
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # HSTS: forzar HTTPS solo en producción
    if os.environ.get('RENDER_EXTERNAL_URL'):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    
    # CSP: política de seguridad de contenido (se complementa con meta tag en base.html)
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net https://www.googletagmanager.com; "
        "style-src 'self' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https://upload.wikimedia.org; "
        "font-src 'self' data:; "
        "connect-src 'self';"
    )
    return response

# ----------------------------
# Manejo de errores personalizado
# ----------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f'Error 500: {e}')
    return render_template('500.html'), 500

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({
        'error': e.name,
        'message': e.description
    }), e.code

# ----------------------------
# Importar y registrar Blueprint
# ----------------------------
from rutas.web import web
app.register_blueprint(web)

# ----------------------------
# Ejecutar la app
# ----------------------------
if __name__ == '__main__':
    # Determinar si estamos en modo debug (NUNCA en producción)
    is_debug = os.environ.get('FLASK_DEBUG', '0') == '1' and not os.environ.get('RENDER_EXTERNAL_URL')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=is_debug)