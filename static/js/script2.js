
if (sessionStorage.getItem('comprador') === "activo") {
    
    document.getElementById("login").style.display = "none";
    document.getElementById("btn-login").style.display = "none";
    document.getElementById("btn-logout").style.display = "block";
}
if (sessionStorage.getItem('comprador') === "no") {
    
    document.getElementById("login").style.display = "block";
    document.getElementById("btn-login").style.display = "block";
    document.getElementById("btn-logout").style.display = "none";
}