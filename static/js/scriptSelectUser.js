// DESPLIEGE DE LA OPCION DEL TIPO DE USUARIO
const selectedUsuario = document.querySelector(".selected-usuario");
const optionsContainerUsuario = document.querySelector(".options-container-usuario");
const optionsListUsuario = document.querySelectorAll(".option-user");

const selectedSexCargo = document.querySelector(".selected-sc");
const optionsContainerSexCargo = document.querySelector(".options-container-sc");
const optionsListSexCargo = document.querySelectorAll(".option-sc");

const selectedCargo = document.querySelector(".selected-cargo");
const optionsContainerCargo = document.querySelector(".options-container-cargo");
const optionsListCargo = document.querySelectorAll(".option-cargo");




selectedUsuario.addEventListener("click", () => {
    if(sessionStorage.getItem('userType')=="superAdmin"){
        optionsContainerUsuario.classList.toggle("active");
    }

});

selectedSexCargo.addEventListener("click", () => {
    if(sessionStorage.getItem('userType')=="superAdmin"){
        optionsContainerSexCargo.classList.toggle("active");
    }

});

selectedCargo.addEventListener("click", () => {
    if(sessionStorage.getItem('userType')=="superAdmin"){
        optionsContainerCargo.classList.toggle("active");
    }

});

optionsListUsuario.forEach(o => {
    o.addEventListener("click", () => {
        selectedUsuario.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerUsuario.classList.remove("active");
        var nombre = document.querySelector(".selected-usuario").textContent;
        document.getElementById("inputSelected").value=nombre;
        
    });
});

optionsListSexCargo.forEach(o => {
    o.addEventListener("click", () => {
        selectedSexCargo.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerSexCargo.classList.remove("active");
        var nombre = document.querySelector(".selected-sc").textContent;
        document.getElementById("inputSelectedSexo").value=nombre;
        
    });
});

optionsListCargo.forEach(o => {
    o.addEventListener("click", () => {
        selectedCargo.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerCargo.classList.remove("active");
        var nombre = document.querySelector(".selected-cargo").textContent;
        document.getElementById("inputSelectedCargo").value=nombre;
        
    });
});


