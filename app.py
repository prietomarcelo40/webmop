from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')  # Cambiamos a servicios.html

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        print(f"Nuevo mensaje de {nombre} ({email}): {mensaje}")
        return "¡Gracias por tu mensaje!"
    return render_template('contacto.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
