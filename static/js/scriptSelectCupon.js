// DESPLIEGE DE LA OPCION DEL TIPO DE CUPON
const selectedCupon = document.querySelector(".selected-cupon");
const optionsContainerCupon = document.querySelector(".options-container-cupon");
const optionsListCupon = document.querySelectorAll(".option-cupon");


selectedCupon.addEventListener("click", () => {
    optionsContainerCupon.classList.toggle("active");
    
});

optionsListCupon.forEach(o => {
    o.addEventListener("click", () => {
        selectedCupon.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerCupon.classList.remove("active");
        var nombre = document.querySelector(".selected-Cupon").textContent;
        document.getElementById("inputSelectedCupon").value=nombre;
        
    });
});
