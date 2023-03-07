from flask import Flask, render_template, request, redirect, url_for
from Modelo import Busqueda

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('busqueda'))


@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    if request.method == 'POST':
        producto = request.form['producto']
        tabla = Busqueda.busqueda_mercado_libre(producto)
        return render_template('muestra.html', lista_producto=tabla)
    else:
        return render_template('busqueda.html')
