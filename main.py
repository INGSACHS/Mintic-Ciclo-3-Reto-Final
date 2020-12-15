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
    cursor.execute('SELECT * FROM TBL_PRODUCTO WHERE CODIGO =2')

    rows = cursor.fetchall()

    for row in rows:
        print(row)
    
    return redirect(url_for('.inventario'))



@app.route('/inventarioGeneral.html')
def inventarioGeneral():
    return render_template('inventarioGeneral.html')

#CREAR NUEVO USUARIO //Validaciones
@app.route( '/register', methods=('GET', 'POST') )
def register():
    username = request.form['name']
    password = request.form['password']
    email = request.form['email']
    
    db = get_db()
    
    if(username != ""):
        if(password != ""):
            if(email != ""):
                db.execute('INSERT INTO TBL_USUARIO (NOMBRE, PASSWORD, EMAIL,ROL) VALUES (?,?,?,?)',
                (username, password, email, 2))
    else:
        pass
    
    db.commit()
    close_db()

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


if __name__ == "__main__":
    app.run(debug = True)
    mail.init_app(app)