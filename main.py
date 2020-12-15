from flask import Flask, render_template, url_for, request, flash, redirect, flash
import smtplib
import json
from flask_mail import Mail
from flask_mail import Message
import sqlite3
from sqlite3 import Error
from flask import g
import os
from db import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice



app = Flask(__name__)
app.config.update(    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'proycafmintic@gmail.com',
    MAIL_PASSWORD = '12345ABcd*',
    )
mail = Mail(app)


@app.route('/')

def index():
    return render_template('index.html')


@app.route('/recuperar', methods=['POST'])

def recuperar():

    email = request.form['email']
    
    msg = Message('Cambio de contraseña', sender= 'proycafmintic@gmail.com',recipients=[email],body="Siga los siguientes pasos para recuperar su contraseña")
    mail.send(msg)
    print(email)
    
    return render_template('recuperar.html')

@app.route('/admin.html')
def administrador():
    return render_template('admin.html')


@app.route('/general.html')
def usuario():
    return render_template('general.html')

@app.route('/inventario.html')
def inventario():
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM TBL_PRODUCTO")
    rows = cursor.fetchall()


    return render_template('inventario.html', rows=rows)

@app.route('/eliminar/<int:idP>', methods=('GET','POST'))
def eliminar(idP):
    #idProducto = request.form['idP']
    print(idP)
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()    
    cursor.execute("delete from TBL_PRODUCTO where CODIGO=?", (idP,))
    con.commit()
    
    return inventario()
    
""" @app.route('/editar/<nombre>/<cantidad>/<desc>', methods=('GET','POST'))
def editar(nombre,cantidad,desc):
    #idProducto = request.form['idP']
    print(nombre )
    print(cantidad)
    print(desc)
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()    
    row=cursor.execute("SELECT * FROM TBL_PRODUCTO WHERE CODIGO= ?", (idP,)).fetchone()
     nombre=row[1]
    id=row[0]
    descripcion=row[3]
    imagen=row[4]        
    return render_template('inventario.html') """

@app.route('/filtrar',methods=('GET','POST'))
def filtrar():
    palabra=request.args.get('Buscar')
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    consulta= "%"+palabra+"%"
    cursor.execute('SELECT * FROM TBL_PRODUCTO where NOMBRE LIKE ?',(consulta,))
    rows = cursor.fetchall()
    print(rows)

    return render_template('inventario.html',rows=rows)


@app.route('/inventarioGeneral.html')
def inventarioGeneral():
    return render_template('inventarioGeneral.html')

#CREAR NUEVO USUARIO //Validaciones
@app.route( '/register', methods=('GET', 'POST') )
def register():
    username = request.form['name']
    password = request.form['password']
    hashpassword= generate_password_hash(password)
    email = request.form['email']
    
    db = get_db()
    
    if(username != ""):
        if(password != ""):
            if(email != ""):
                db.execute('INSERT INTO TBL_USUARIO (NOMBRE, PASSWORD, EMAIL,ROL) VALUES (?,?,?,?)',
                (username, hashpassword, email, 2))
                cuerpo_mensaje="Su correo ha sido registrado, su contraseña de ingreso es "+password
                msg = Message('Usuario registrado', sender= 'proycafmintic@gmail.com',recipients=[email],body=cuerpo_mensaje)
                mail.send(msg)
    else:
        pass
    
    db.commit()
    close_db()    
    
    
    print(email)

    return redirect(url_for('.administrador'))

#CREAR NUEVO PRODUCTO //Validaciones
@app.route( '/producto', methods=('GET', 'POST') )
def new_product():
    name_producto = request.form['namep']
    quantity = request.form['quantity'] 
    description = request.form['description']
    photo = request.form['photo']
    print(name_producto)
    db = get_db()
    
    
    if(name_producto != ""):
        if(quantity != ""):
            if(description != ""):
                db.execute('INSERT INTO TBL_PRODUCTO (NOMBRE, CANTIDAD, DESCRIPCION , IMAGEN) VALUES (?,?,?,?)',
                (name_producto, quantity, description, photo))

                
    else:
        pass
    
    db.commit()
    close_db()

    return redirect(url_for('.administrador'))


#validar usuario en el login
@app.route('/validarUsuario',methods=('GET','POST'))
def validarUsuario():
    if request.method == 'POST':
            db = get_db()
            error = None
            username = request.form['correo']
            print(username)
            password2 = request.form['password']

            if not username:
                error = 'Debes ingresar el usuario'
                flash(error)
                return render_template('index.html', error="error")

            if not password2:
                error = 'Contraseña requerida'
                flash(error)
                return render_template('index.html', error="error")

            user = db.execute(
                'SELECT * FROM TBL_USUARIO WHERE EMAIL = ?', (username,)).fetchone()

            if user is None:
                error = 'Usuario o contraseña inválidos'
            else:
                if check_password_hash(user[2],password2):
                    if (user[4] == 1):
                        return render_template('admin.html')
                    else:
                        return usuario()

            
    return render_template('index.html', error="error")

""" @app.route('/mirar')
def mirar()
longitud=8
valores="0123456789abcdefghijklmnoqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@&%+"
p=""
p= p.join([choice(valores) for i in range(longitud)])
return p 



@app.route('/contrasena', method="POST")
def contraseña():

    password=request.form['password']
    hashpassword= generate_password_hash(password)
    ##if check password_hash(user['contraseña],password)
    return hashpassword """



if __name__ == "__main__":
    app.run(debug = True)
    mail.init_app(app)