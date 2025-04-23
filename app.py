from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Cargar los cascos desde el archivo JSON
def cargar_cascos():
    with open("cascos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

@app.route("/")
def index():
    cascos = cargar_cascos()
    return render_template("index.html", cascos=cascos)

@app.route("/cascos")
def cascos():
    cascos = cargar_cascos()
    return render_template("cascos.html", cascos=cascos)

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")
    
@app.route("/contacto")
def contacto():
    return render_template("contacto.html")
    
@app.route("/faq")
def faq():
    return render_template("faq.html")
    
    
@app.route("/proteccion_datos")
def proteccion_datos():
    return render_template("proteccion_datos.html")

@app.route("/casco/<nombre>")
def casco_individual(nombre):
    cascos = cargar_cascos()
    casco = next((c for c in cascos if c["nombre"].lower().replace(" ", "_") == nombre.lower()), None)
    if casco:
        return render_template("casco_individual.html", casco=casco)
    return "Casco no encontrado", 404

if __name__ == "__main__":
    app.run(debug=True)
