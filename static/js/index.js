window.onload = function(){
    sliderUno();
    sliderDos();
}

let sliderOne = document.getElementById("slider");
let sliderTwo = document.getElementById("slider2");
let displayValOne = document.getElementById("price-range1");
let displayValTwo = document.getElementById("price-range2");
let minGap = 0;
let sliderTrack = document.querySelector(".priceContainer-sliderTrack");
let sliderMaxValue = document.getElementById("slider").max;

function sliderUno(){
    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    displayValOne.textContent = sliderOne.value;
    fillColor();
}
function sliderDos(){
    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    displayValTwo.textContent = sliderTwo.value;
    fillColor();
}

function fillColor(){
    percent1 = (sliderOne.value / sliderMaxValue) * 100;
    percent2 = (sliderTwo.value / sliderMaxValue) * 100;
    sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , black ${percent1}% , black ${percent2}%, #dadae5 ${percent2}%)`;
}
