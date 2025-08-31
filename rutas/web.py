import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from flask import Blueprint, render_template, abort, request, redirect, url_for

# Carga las variables del archivo .env al entorno
load_dotenv()

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')

PAGES = {
    'index': 'index.html',
    'servicios': 'servicios.html',
    'trabajos': 'trabajos.html',
    'contacto': 'contacto.html',
}

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/<page>')
def show_page(page):
    if page in PAGES:
        return render_template(PAGES[page])
    else:
        abort(404)

# Nueva ruta para procesar el formulario de contacto
@web.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email_remitente = request.form.get('email')
        mensaje = request.form.get('mensaje')

        # Configuración del email usando variables de entorno
        email_sender = os.getenv('EMAIL_REMITENTE')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_receiver = email_sender

        subject = f'Nuevo mensaje de contacto de: {nombre}'
        body = f"""
        Hola,
        Has recibido un nuevo mensaje desde el formulario de contacto de tu sitio web.

        Nombre: {nombre}
        Email: {email_remitente}
        Mensaje:
        {mensaje}
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                print("Correo enviado exitosamente.")
                return redirect(url_for('web.show_page', page='contacto', enviado='success'))
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            return redirect(url_for('web.show_page', page='contacto', enviado='error'))

    return redirect(url_for('web.show_page', page='contacto'))