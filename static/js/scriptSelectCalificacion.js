// DESPLIEGE DE LA OPCION DE LA CALIFICACION
const selectedCalificacion = document.querySelector(".selected-calificacion");
const optionsContainerCalificacion = document.querySelector(".options-container-calificacion");
const optionsListCalificacion = document.querySelectorAll(".option-calificacion");

selectedCalificacion.addEventListener("click", () => {
    optionsContainerCalificacion.classList.toggle("active");
});

optionsListCalificacion.forEach(o => {
    o.addEventListener("click", () => {
        selectedCalificacion.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerCalificacion.classList.remove("active");
        var nombre = document.querySelector(".selected-calificacion").textContent;
        document.getElementById("inputSelectedCalificacion").value=nombre;
    });
});

// DESPLIEGE DE LA OPCION DE LA UNIDAD
const selectedUnidad = document.querySelector(".selected-unidad");
const optionsContainerUnidad = document.querySelector(".options-container-unidad");
const optionsListUnidad = document.querySelectorAll(".option-unidad");

selectedUnidad.addEventListener("click", () => {
    optionsContainerUnidad.classList.toggle("active");
});

optionsListUnidad.forEach(o => {
    o.addEventListener("click", () => {
        selectedUnidad.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerUnidad.classList.remove("active");
        var nombre = document.querySelector(".selected-unidad").textContent;
        document.getElementById("inputSelectedUnidad").value=nombre;
        
    });
});

// DESPLIEGE DE LA OPCION DEL LOTE
const selectedLote = document.querySelector(".selected-lote");
const optionsContainerLote = document.querySelector(".options-container-lote");
const optionsListLote = document.querySelectorAll(".option-lote");

selectedLote.addEventListener("click", () => {
    optionsContainerLote.classList.toggle("active");
});

optionsListLote.forEach(o => {
    o.addEventListener("click", () => {
        selectedLote.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerLote.classList.remove("active");
        var nombre = document.querySelector(".selected-lote").textContent;
        document.getElementById("inputSelectedLote").value=nombre;
        
    });
});