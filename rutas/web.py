from flask import Blueprint, render_template, abort, request, redirect, url_for
import smtplib
import ssl
from email.message import EmailMessage

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
        # 1. Recoger los datos del formulario
        nombre = request.form.get('nombre')
        email_remitente = request.form.get('email')
        mensaje = request.form.get('mensaje')
        
        # 2. Configurar los detalles del email
        # RECUERDA: Cambiar estos valores por tu correo y contraseña de aplicación
        # Para Gmail, necesitas generar una 'contraseña de aplicación' en la configuración de seguridad.
        email_sender = 'prietomarcelo40@gmail.com' 
        email_password = 'lmhx artw sgpi ppmt' 
        email_receiver = 'prietomarcelo40@gmail.com' # Puedes poner un correo diferente si lo deseas

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
            # 3. Enviar el correo electrónico
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                print("Correo enviado exitosamente.")
                # Redirige al  a la página de contacto con un mensaje de éxito
                # (Necesitarías manejar este mensaje en tu HTML)
                return redirect(url_for('web.show_page', page='contacto', enviado='success'))
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            # Redirige al usuario con un mensaje de error
            return redirect(url_for('web.show_page', page='contacto', enviado='error'))

    # Si la solicitud no es POST, simplemente redirige a la página de contacto
    return redirect(url_for('web.show_page', page='contacto'))