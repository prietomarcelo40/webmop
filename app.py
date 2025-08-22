from flask import Flask, render_template, request
import os

app = Flask(__name__, static_folder='static')

# -----------------------
# Rutas de la web
# -----------------------
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/trabajos')
def trabajos():
    return render_template('trabajos.html')

# -----------------------
# Ejecutar la app
# -----------------------
if __name__ == '__main__':
    # Fly.io asigna el puerto en la variable PORT
    port = int(os.environ.get("PORT", 5000))

    # Debug activo solo si la variable FLASK_DEBUG es "1" o no existe (local)
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Host 0.0.0.0 para exponer la app en contenedores (Fly.io)
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
