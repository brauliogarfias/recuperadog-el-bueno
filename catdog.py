#PROGRAMA PRINCIPAL 


from contextlib import nullcontext



import os
from flask import Flask, send_from_directory, redirect, url_for ,render_template, request, session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
import pymongo
import qrcode
import datetime

app = Flask(__name__)

app.secret_key = 'tu_clave_secreta'  # Asegúrate de cambiar esto por una clave segura en un entorno de producción


CONNECTION_STRING ="mongodb+srv://catdog-23:Admin_8723@cluster0.wf7ii.mongodb.net/"

client = MongoClient(CONNECTION_STRING)

test=client.test

db = client.CatDog

coleccion = db.Mascota


app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['UPLOAD_FOLDER_INE'] = 'static/images/INE'
app.config['UPLOAD_FOLDER_DOM'] = 'static/images/CompD'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


load_dotenv()
#Configuracion de la extension Flask-Mail para usar Gmail 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'recuperadog.y.rescate@gmail.com'  
app.config['MAIL_PASSWORD'] = os.getenv('LLAVE')  
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



no_mascota = 0
mascotas = {}


@app.route("/")
def home():
    return render_template("base.html")


@app.route('/agregar_mascota', methods = ['POST', 'GET'])
def agregar_mascota():
    
    if request.method == 'POST':
        


        id_propietario=session['nombre']
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
        checkbox = request.form['checkbox'] 
       
        file = request.files['archivo']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        filename = 'images/' + filename

        global no_mascota
        no_mascota += 1
        id_mascota = (str(no_mascota))

        tiempo_actual = datetime.datetime.now()
        id_mascota= (str(tiempo_actual.year)+str(tiempo_actual.month)+str(tiempo_actual.day)+str(tiempo_actual.hour)+str(tiempo_actual.minute)+str(tiempo_actual.second)+str(tiempo_actual.microsecond))
        

        


        nueva_mascota = {
            "id_mascota": id_mascota,
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
            "filename" : filename,
            "adopcion" : checkbox,
            "QR" : id_mascota,
            "propietario":id_propietario

            
        }

       
        coleccion.insert_one(nueva_mascota)

        crear_qr(id_mascota)
        enviar_correo()
        
        #datos = (nombre, raza, sexo, caracter, color, edad, tamanio, salud, sociable, contacto, filename)
        #return redirect(url_for("lista", data=datos))
        
        data=[]
        data.append (nueva_mascota )
        
        return render_template("seguimiento.html",data=data)
       
        
        
    
    else:
        return render_template("agregar.html")
     

@app.route('/galeria', methods = ['POST', 'GET'])
def galeria(data=[]):

    data=[]
    PET=coleccion.find({'adopcion': "SI"})
    
    for pets in PET:
        data.append(pets)

    return render_template("galeria.html", dic = data)

def crear_qr(mascota_id):

    id_mascota = mascota_id
  
    host =   "http://127.0.0.1:5000/seguimiento2/"
    
    data = host + id_mascota
 
    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version = 1,
                   box_size = 20,
                   border = 5)
 
    # Adding data to the instance 'qr'
    qr.add_data(data)
 
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'red',
                    back_color = 'white')
    
    
    
    
    img.save(   os.path.join(app.config['UPLOAD_FOLDER'], str(id_mascota)+".png")   )

def enviar_correo():
        msg = Message('Bienvenidos a Recuperadog y Rescate', sender='recuperadog.y.rescate@gmail.com', recipients=[  str(session['nombre']) ]     )
        msg.body = '''Te has registrado, ahora puedes navegar por la pagina Recuperadog y Rescate con libertad'''
        mail.send(msg)


        print('Correo enviado :3 a', str(session['nombre']) )    

    
@app.route('/login', methods = ['POST', 'GET'])
def login(data=[]):

    if request.method == 'POST':
       
        nombre = request.form['nombre']
        password = request.form['password']

        USER = db.Usuario.find({
            "$and": [
                {"correo": nombre},
                {"password": password}
            ]
        })
       
        data=[]

        listaUsuarios=list(USER)
        if len(listaUsuarios)!=0:
            username=""
            
            username = request.form['nombre']
            session['nombre'] = username
            data.append(USER)
            data.append(username)
            return render_template("base.html")    
        
        
    else:
        print(request.method)

            
    
    
    return render_template('login.html',dic=data)
    

    
@app.route('/logout', methods = ['POST', 'GET'])
def logout(data=[]):
    session.pop('nombre', None)
    return redirect('/login')
        

   
@app.route('/chat', methods = ['POST', 'GET'])
def chat(data=[]):

    id_login=["idLogin",1]
    id_mascota=["idMascota",2]


    data.append(id_login)
    data.append(id_mascota)


    return render_template("chat.html",dic = data)



@app.route('/signin', methods = ['POST', 'GET'])
def signin(data=[]):


    
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        celular = request.form['celular']
        correo = request.form['correo']
        contrasela = request.form['contrasela']
        colonia = request.form['colonia']
        calle = request.form['calle']
        
        
        
        file1 = request.files['ine']
        filename1 = secure_filename(file1.filename)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER_INE'], filename1))
        filename1 = 'images/INE/' + filename1

        file2 = request.files['comprobanteDomicilio']
        filename2 = secure_filename(file2.filename)
        file2.save(os.path.join(app.config['UPLOAD_FOLDER_DOM'], filename2))
        filename2 = 'images/CompD/' + filename2

        nuevo_usuario = {
            "nombre" : nombre,
            "celular" : celular,
            "correo" : correo,
            "password" : contrasela,
            "colonia" : colonia,
            "calle" : calle,

            "INE_URL" : filename1,
            "comprobante_domicilio_URL" : filename2
                   
        }

    
        coleccion = db.Usuario

        coleccion.insert_one(nuevo_usuario)

        data=["Usuario Registrado"]
        
        return render_template("base.html")
        
        
    
    else:
         return render_template("signin.html",dic = data)



   
@app.route('/seguimiento', methods = ['POST', 'GET'])
def seguimiento(data=[]):


    return render_template("seguimiento.html",dic = data)




@app.route('/seguimiento2/<id_mascota>')
def seguimiento2(id_mascota):

    
    
    
    data=[]
    PET=coleccion.find({'id_mascota': id_mascota})
    
    correo=""
    for pets in PET:
        clave, valor = pets.popitem()
        print(clave, valor)
        if(clave=="propietario"):
            correo=valor
        data.append(pets)
    

    data2=[]
    colleccion2 = db.Usuario
    USR=colleccion2.find({'correo': correo})
    for usr in USR:
        print(usr)
        data2.append(usr)
    
    #return f'El valor de id_mascota es: {data}'
    return render_template("seguimiento.html",data = data,data2 = data2)
    
    
    
if __name__ == '__main__':   
    app.run(threaded= True, debug = True)
    

# `task_func` is PyWebIO task function
#app.add_url_rule('/tool', 'webio_view', webio_view(home),
#            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods



