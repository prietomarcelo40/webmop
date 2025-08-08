from flask import Flask, render_template, request

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
    app.run(debug=True)
