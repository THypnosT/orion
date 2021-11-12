// DESPLIEGE DE LA OPCION DEL TIPO DE USUARIO
const selectedSexo = document.querySelector(".selected-sexo");
const optionsContainerSexo = document.querySelector(".options-container-sexo");
const optionsListSexo = document.querySelectorAll(".option-sexo");


selectedSexo.addEventListener("click", () => {
    optionsContainerSexo.classList.toggle("active");
 
});

optionsListSexo.forEach(o => {
    o.addEventListener("click", () => {
        selectedSexo.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerSexo.classList.remove("active");
        var nombre = document.querySelector(".selected-sexo").textContent;
        document.getElementById("inputSelectedSexo").value=nombre;
        
    });
});
