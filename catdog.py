#PROGRAMA PRINCIPAL - CATDOG


from contextlib import nullcontext


import os
from flask import Flask, send_from_directory, redirect, url_for ,render_template, request
from werkzeug.utils import secure_filename

from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
import pymongo



app = Flask(__name__)

CONNECTION_STRING ="mongodb+srv://catdog-23:Admin_8723@cluster0.wf7ii.mongodb.net/"

client = MongoClient(CONNECTION_STRING)

db = client.CatDog

coleccion = db.Mascota


app.config['UPLOAD_FOLDER'] = 'static/images'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


no_mascota = 0
mascotas = {}



@app.route("/")
def home():
    return render_template("base.html")


@app.route('/agregar_mascota', methods = ['POST', 'GET'])
def agregar_mascota():
    
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        raza = request.form['raza']
        sexo = request.form['sexo']
        caracter = request.form['caracter']
        color = request.form['color']
        edad = request.form['edad']
        tamanio = request.form['tamanio']
        salud = request.form['salud']
        sociable = request.form['sociable']
        contacto = request.form['contacto']
       
        file = request.files['archivo']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        filename = 'images/' + filename

        global no_mascota
        no_mascota += 1
        id_mascota = (str(no_mascota))
        nueva_mascota = {
            "nombre" : nombre,
            "raza" : raza,
            "sexo" : sexo,
            "caracter" : caracter,
            "color" : color,
            "edad" : edad,
            "tamanio" : tamanio,
            "salud" : salud,
            "sociable" : sociable,
            "contacto" : contacto,
            "filename" : filename
            
        }

        mascotas.update({id_mascota : nueva_mascota})

       
        coleccion.insert_one(nueva_mascota)
        
        #datos = (nombre, raza, sexo, caracter, color, edad, tamanio, salud, sociable, contacto, filename)
        #return redirect(url_for("lista", data=datos))
        return galeria(data=mascotas)
        
        
    
    else:
        return render_template("agregar.html")
     

@app.route('/galeria', methods = ['POST', 'GET'])
def galeria(data={}):
    
    print(data)
    return render_template("galeria.html", dic = data)
    
    
    
if __name__ == '__main__':   
    app.run(threaded= True, debug = True) 
    

# `task_func` is PyWebIO task function
#app.add_url_rule('/tool', 'webio_view', webio_view(home),
#            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods



