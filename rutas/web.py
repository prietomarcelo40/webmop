from flask import Blueprint, render_template, redirect, url_for, flash
from flask_mail import Message
from .forms import ContactoForm
import bleach
import os

# ----------------------------
# Definir Blueprint
# ----------------------------
web = Blueprint('web', __name__)

# ----------------------------
# Rutas
# ----------------------------
@web.route('/')
def inicio():
    return render_template('inicio.html')

@web.route('/servicios')
def servicios():
    return render_template('servicios.html')

@web.route('/trabajos')
def trabajos():
    return render_template('trabajos.html')

@web.route('/contacto', methods=['GET', 'POST'])
def contacto():
    # Importar app, mail y limiter dentro de la función para evitar circular imports
    from app import app, mail, limiter

    # Aplicar limitador dentro de la función
    @limiter.limit("5 per minute")
    def procesar_formulario():
        form = ContactoForm()
        if form.validate_on_submit():
            nombre = form.nombre.data.strip()
            email = form.email.data.strip()
            mensaje = bleach.clean(form.mensaje.data, tags=[], attributes={}, strip=True)

            msg = Message(
                subject='Mensaje de contacto de Mi Web',
                sender=app.config['MAIL_USERNAME'],
                recipients=[os.environ.get('EMAIL_DESTINATARIO', app.config['MAIL_USERNAME'])],
                body=f'De: {nombre}\nCorreo: {email}\nMensaje:\n{mensaje}'
            )

            try:
                mail.send(msg)
                flash('¡Mensaje enviado con éxito!', 'success')
                app.logger.info(f'Mensaje enviado: {nombre} - {email}')
            except Exception as e:
                flash('Hubo un problema al enviar tu mensaje.', 'danger')
                app.logger.error(f'Error al enviar correo: {e}')

            return redirect(url_for('web.contacto'))

        return render_template('contacto.html', form=form)

    return procesar_formulario()
