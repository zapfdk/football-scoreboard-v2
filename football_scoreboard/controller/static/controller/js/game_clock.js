'use strict';
let submitClockButton = document.getElementById('submit_clock');
let clockInput = document.getElementById('clock_input');
let clock = document.getElementById('clock');
let toggleButton = document.getElementById('toggle_button');
let status = document.getElementById('status');
let color = false;

submitClockButton.addEventListener('click', function(event) {
    let clockValue = clockInput.value;
    clock.innerHTML = clockValue;
});

toggleButton.addEventListener('click', function(event) {
    if (color) {
        status.style.backgroundColor = "#ff0000";
    }
    else {
        status.style.backgroundColor = "#00ff00";
    }
    color = !color;
});