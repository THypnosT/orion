// DESPLIEGE DE LA OPCION DEL TIPO DE USUARIO
const selectedSexo = document.querySelector(".selected");
const optionsContainerSexo = document.querySelector(".options-container");
const optionsListSexo = document.querySelectorAll(".option");


selectedSexo.addEventListener("click", () => {
    optionsContainerSexo.classList.toggle("active");
 
});

optionsListSexo.forEach(o => {
    o.addEventListener("click", () => {
        selectedSexo.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerSexo.classList.remove("active");
        var nombre = document.querySelector(".selected").textContent;
        document.getElementById("inputSelectedSearch").value=nombre;
        
    });
});
