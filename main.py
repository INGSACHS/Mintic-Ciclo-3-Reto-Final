import functools
from flask import Flask, render_template, url_for, request, flash, redirect, flash, session, g
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
app.config.update(MAIL_SERVER='smtp.gmail.com',
                  MAIL_PORT=587,
                  MAIL_USE_TLS=True,
                  MAIL_USE_SSL=False,
                  MAIL_USERNAME='proycafmintic@gmail.com',
                  MAIL_PASSWORD='12345ABcd*',
                  )
mail = Mail(app)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = os.path.abspath("./resources/")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))
        return view(**kwargs)
    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM TBL_USUARIO WHERE CODIGO = ?', (user_id,)
        ).fetchone()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recuperar', methods=['POST'])
@login_required
def recuperar():

    email = request.form['email']

    msg = Message('Cambio de contraseña', sender='proycafmintic@gmail.com',
                  recipients=[email], body="Siga los siguientes pasos para recuperar su contraseña")
    mail.send(msg)
    print(email)

    return render_template('recuperar.html')


@app.route('/admin.html')
@login_required
def administrador():
    return render_template('admin.html')


@app.route('/general.html')
@login_required
def usuario():

    return render_template('general.html')


@app.route('/inventario.html')
@login_required
def inventario():
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM TBL_PRODUCTO")
    rows = cursor.fetchall()

    return render_template('inventario.html', rows=rows)


@app.route('/inventarioGeneral.html')
@login_required
def inventarioGeneral():
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM TBL_PRODUCTO")
    listas = cursor.fetchall()

    return render_template('inventarioGeneral.html', listas=listas)


@app.route('/eliminar/<int:idP>', methods=('GET', 'POST'))
@login_required
def eliminar(idP):
    # idProducto = request.form['idP']
    print(idP)
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    cursor.execute("delete from TBL_PRODUCTO where CODIGO=?", (idP,))
    con.commit()

    return inventario()

# metodo de buscar en rol "administrador"


@app.route('/filtrar', methods=('GET', 'POST'))
@login_required
def filtrar():
    palabra = request.args.get('Buscar')
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    consulta = "%"+palabra+"%"
    cursor.execute(
        'SELECT * FROM TBL_PRODUCTO where NOMBRE LIKE ?', (consulta,))
    rows = cursor.fetchall()

    return render_template('inventario.html', rows=rows)

# metodo de buscar en rol "usuario"


@app.route('/filtrarG', methods=('GET', 'POST'))
@login_required
def filtrarG():
    palabra = request.args.get('Buscar')
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    consulta = "%"+palabra+"%"
    cursor.execute(
        'SELECT * FROM TBL_PRODUCTO where NOMBRE LIKE ?', (consulta,))
    listas = cursor.fetchall()

    return render_template('inventarioGeneral.html', listas=listas)


# CREAR NUEVO USUARIO //Validaciones


@app.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    username = request.form['name']
    password = request.form['password']
    hashpassword = generate_password_hash(password)
    email = request.form['email']

    db = get_db()

    if(username != ""):
        if(password != ""):
            if(email != ""):
                db.execute('INSERT INTO TBL_USUARIO (NOMBRE, PASSWORD, EMAIL,ROL) VALUES (?,?,?,?)',
                           (username, hashpassword, email, 2))
                cuerpo_mensaje = "Su correo ha sido registrado, su contraseña de ingreso es "+password
                msg = Message('Usuario registrado', sender='proycafmintic@gmail.com',
                              recipients=[email], body=cuerpo_mensaje)
                mail.send(msg)
    else:
        pass

    db.commit()
    close_db()

    print(email)

    return redirect(url_for('.administrador'))

# CREAR NUEVO PRODUCTO //Validaciones


@app.route('/producto', methods=('GET', 'POST'))
@login_required
def new_product():
    name_producto = request.form['namep']
    quantity = request.form['quantity']
    description = request.form['description']
    foto = request.form['photo']
    print(name_producto)
    db = get_db()
    ruta = "../static/img/"+foto
    if(name_producto != ""):
        if(quantity != ""):
            if(description != ""):
                db.execute('INSERT INTO TBL_PRODUCTO (NOMBRE, CANTIDAD, DESCRIPCION, IMAGEN ) VALUES (?,?,?,?)',
                           (name_producto, quantity, description, ruta))

    else:
        pass

    db.commit()
    close_db()

    return redirect(url_for('.administrador'))

# Actualizar producto


@app.route('/actualizar/<int:idP>/', methods=('GET', 'POST'))
@login_required
def actualizar(idP):
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM TBL_PRODUCTO WHERE CODIGO= ?", (idP,))
    producto = cursor.fetchone()
    return render_template('actualizar2.html', producto=producto)

# actualizar cantidad rol "usuario"


@app.route('/actualizarG/<int:idP>/', methods=('GET', 'POST'))
@login_required
def actualizarG(idP):
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM TBL_PRODUCTO WHERE CODIGO= ?", (idP,))
    producto = cursor.fetchone()

    return render_template('actualizarG.html', producto=producto)

# guardar actualizacion del producto rol "administrador"


@app.route('/saveProducto', methods=('GET', 'POST'))
def saveProducto():
    name_producto = request.form['namep']
    quantity = request.form['quantity']
    description = request.form['description']
    idP = request.form['idP']
    imagen = request.form['picture']
    ruta2 = "../static/img/" + imagen
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()
    if (ruta2 == "../static/img/"):
        cursor.execute(
            "UPDATE TBL_PRODUCTO SET NOMBRE= ?, CANTIDAD=?, DESCRIPCION=? where CODIGO=?", (name_producto, quantity, description, idP,))
        con.commit()
    else:
        cursor.execute(
            "UPDATE TBL_PRODUCTO SET NOMBRE= ?, CANTIDAD=?, DESCRIPCION=?, IMAGEN=? where CODIGO=?", (name_producto, quantity, description, ruta2, idP,))
        con.commit()

    return inventario()

# guardar actualizacion rol"usuario"


@app.route('/saveProductoG', methods=('GET', 'POST'))
def saveProductoG():
    quantity = request.form['quantity']
    idP = request.form['idP']
    con = sqlite3.connect('Inventario.db')
    cursor = con.cursor()

    cursor.execute(
        "UPDATE TBL_PRODUCTO SET CANTIDAD=? where CODIGO=?", (quantity, idP,))
    con.commit()
    return inventarioGeneral()

# validar usuario en el login


@app.route('/validarUsuario', methods=('GET', 'POST'))
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
            if check_password_hash(user[2], password2):
                session.clear()
                if (user[4] == 1):
                    session['user_id'] = user[4]
                    return render_template('admin.html')

                else:
                    session['user_id'] = user[4]
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
    # if check password_hash(user['contraseña],password)
    return hashpassword """


if __name__ == "__main__":
    app.run(debug=True)
    mail.init_app(app)
