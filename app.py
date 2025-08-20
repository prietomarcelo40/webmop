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
    # Puerto asignado por Render, por defecto 5000 para desarrollo local
    port = int(os.environ.get("PORT", 5000))

    # Debug activo solo si la variable FLASK_DEBUG es "1" o no existe (local)
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Host 0.0.0.0 para que Render pueda exponer la app
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
