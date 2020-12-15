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