//Función para mostrar y cerrar el popup de olvido contraseña
function mostrarPopup() {
    document.getElementById("popup").classList.toggle("active");
}

//Función para mostrar la página siguiente al logeo
function mostrarPagina(opcion) {
    if (opcion == 1) {
        window.open("../admin.html", "_self");
    } else {
        window.open("../general.html", "_self");
    }
    return false;
}

//Función para vaidar los datos ingresados en los campos del login
function validarDatosFormularioLogin() {

    //Variables
    let expresion_contraseña = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])([A-Za-z\d$@$!%*?&]|[^ ]){8,15}$/;
    let user = document.getElementById("username");
    let pass = document.getElementById("password");

    //Validar los datos ingresados
    if (user.value != null) {
        if (user.value.length == 0 || user.value.length > 5) {
            if (!(/^\s+$/.test(user.value))) {
                if (pass.value != null) {
                    if (!(/^\s+$/.test(pass.value))) {
                        if (pass.value.match(expresion_contraseña)) {
                            if (user.value == "administrador") {
                                mostrarPagina(1);
                            } else if (user.value == "cliente") {
                                mostrarPagina(2);
                            }
                            alert("Usuario: " + user.value + "\nContraseña: " + pass.value);
                            mostrarPagina();
                        } else {
                            alert("La contraseña debe tener: \nMinimo 8 caracteres, \nMaximo 15 caracteres, \nAl menos una letra mayúscula, \nAl menos una letra minucula, \nAl menos un dígito, \nNo debe tener espacios en blanco, \nAl menos 1 caracter especial");
                            pass.value = "";
                        }
                    } else {
                        alert("Debe ingresar una contraseña valida");
                        pass.value = "";
                    }
                } else {
                    alert("El campo 'Contraseña' no debe estar en blanco");
                }
            } else {
                alert("Debe ingresar un usuario valido");
                user.value = "";
            }
        } else {
            alert("Debe ingresar un usuario con mínimo 8 caracteres");
            user.value = "";
        }
    } else {
        alert("El campo 'Nombre' no debe estar en blanco");
    }

    return false;

}

//Función para vaidar los datos ingresados en el campo del popup
function validarDatosFormularioPassword() {

    //Variables
    let formatoCorreo = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
    let email = document.getElementById("email")

    //Validar los datos ingresados
    if (email.value != "") {
        console.log(email.value);
        if (!(/^\s+$/.test(email.value))) {
            if (email.value.match(formatoCorreo)) {
                alert("Correo electrónico: " + email.value);
            } else {
                alert("EL correo electrónico ingresado es invalido. Ingrese nuevamente el correo");
            }
        } else {
            alert("Debe ingresar un correo electrónico valido");
            email.value = "";
        }
    } else {
        alert("El campo 'Correo electrónico' no debe estar en blanco");
    }

    return false;

}