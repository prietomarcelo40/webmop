from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class ContactoForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(), Length(min=10)])