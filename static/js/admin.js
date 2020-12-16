function openSection(evt, sectionName) {
    var i, x, y;
    x = document.getElementsByClassName("seccion");
    y = document.getElementById("welcome");

    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    document.getElementById(sectionName).style.display = "block";

    if (y.style.display === "none") {
        y.style.display = "none";
    } else {
        y.style.display = "none";
    }
}

function togglePopup() {
    document.getElementById("popup-1").classList.toggle("active");
}

function myFunction(divid) {

    var x = document.getElementById('show' + divid);

    if (x.style.display == "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function habilitar(id) {

    if (document.getElementById('show1' + id).disabled == true) {
        document.getElementById('show1' + id).disabled = false;
    } else {
        document.getElementById('show1' + id).disabled = true;
    }

    if (document.getElementById('show2' + id).disabled == true) {
        document.getElementById('show2' + id).disabled = false;
    } else {
        document.getElementById('show2' + id).disabled = true;
    }

    if (document.getElementById('show3' + id).disabled == true) {
        document.getElementById('show3' + id).disabled = false;
    } else {
        document.getElementById('show3' + id).disabled = true;
    }

}