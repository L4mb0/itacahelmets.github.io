from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import json
import os
from werkzeug.security import generate_password_hash
import datetime

app = Flask(__name__)
# Configuración de clave secreta para flash messages y protección CSRF
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_temporal')

# Cargar los cascos desde el archivo JSON
def cargar_cascos():
    with open("cascos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# Función para guardar suscripciones
def guardar_suscripcion(email):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Crear el archivo si no existe
        if not os.path.exists('suscripciones.json'):
            with open('suscripciones.json', 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Leer las suscripciones existentes
        with open('suscripciones.json', 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
        
        # Verificar si el email ya existe
        for sub in suscripciones:
            if sub['email'] == email:
                return False  # Email ya registrado
        
        # Agregar nueva suscripción
        suscripciones.append({
            'email': email,
            'fecha': fecha
        })
        
        # Guardar suscripciones actualizadas
        with open('suscripciones.json', 'w', encoding='utf-8') as f:
            json.dump(suscripciones, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"Error al guardar suscripción: {e}")
        return False

# Función para guardar mensajes de contacto
def guardar_contacto(nombre, email, mensaje, acepto_terminos):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Crear el archivo si no existe
        if not os.path.exists('contactos.json'):
            with open('contactos.json', 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Leer los contactos existentes
        with open('contactos.json', 'r', encoding='utf-8') as f:
            contactos = json.load(f)
        
        # Agregar nuevo contacto
        contactos.append({
            'nombre': nombre,
            'email': email,
            'mensaje': mensaje,
            'acepto_terminos': acepto_terminos,
            'fecha': fecha
        })
        
        # Guardar contactos actualizados
        with open('contactos.json', 'w', encoding='utf-8') as f:
            json.dump(contactos, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"Error al guardar contacto: {e}")
        return False

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

# Nuevas rutas para procesar formularios

@app.route("/subscribe", methods=["POST"])
def subscribe():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        
        # Validar email
        if not email or '@' not in email:
            flash("Por favor, introduce un email válido.", "error")
            return redirect(request.referrer or url_for('index'))
        
        # Guardar suscripción
        if guardar_suscripcion(email):
            flash("¡Gracias por suscribirte! Pronto recibirás nuestro catálogo.", "success")
        else:
            flash("Este email ya está registrado o hubo un problema al procesar tu solicitud.", "error")
        
        # Redirigir a la página de origen
        return redirect(request.referrer or url_for('index'))

@app.route("/contact", methods=["POST"])
def contact():
    if request.method == "POST":
        nombre = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        mensaje = request.form.get("message", "").strip()
        acepto_terminos = 'accept_terms' in request.form
        
        # Validar campos
        if not nombre or not email or not mensaje:
            flash("Por favor, completa todos los campos.", "error")
            return redirect(url_for('contacto'))
        
        if not acepto_terminos:
            flash("Debes aceptar los términos y condiciones.", "error")
            return redirect(url_for('contacto'))
        
        # Guardar mensaje de contacto
        if guardar_contacto(nombre, email, mensaje, acepto_terminos):
            flash("¡Gracias por contactarnos! Te responderemos a la brevedad.", "success")
        else:
            flash("Hubo un problema al procesar tu mensaje. Por favor, intenta de nuevo.", "error")
        
        return redirect(url_for('contacto'))

if __name__ == "__main__":
    app.run(debug=True)