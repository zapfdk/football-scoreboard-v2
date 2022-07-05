'use strict';
let submitClockButton = document.getElementById('submit_clock');
let clockInput = document.getElementById('clock_input');
let clock = document.getElementById('clock');
let toggleButton = document.getElementById('toggle_button');
let status = document.getElementById('status');
let resetQuarterButton = document.getElementById('reset_quarter');
let color = false;


var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/clock_controller/');

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let time = data["time"];
    let running = data["running"];
    updateStatusDisplay(time, running);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function sendControl(command, value){
    chatSocket.send(JSON.stringify({
        command: command,
        value: value
    }));
}

function updateStatusDisplay(time, running){
    let minutes = Math.floor(time/60);
    let seconds = time % 60;
    let timeFormatted = minutes.toString().padStart(2, '0')+":"+seconds.toString().padStart(2, '0');

    document.getElementById("clock").innerText = timeFormatted;

    if (running) {
        status.style.backgroundColor = "#00ff00";
    }
    else {
        status.style.backgroundColor = "#ff0000";
    }
}

submitClockButton.addEventListener('click', function(event) {
    let clockValue = clockInput.value;
    sendControl("SET_CLOCK", clockValue);
});

function toggleClock() {
    sendControl("TOGGLE_CLOCK", 0);
};

toggleButton.addEventListener('click', function(event) {
    toggleClock();
});

resetQuarterButton.addEventListener('click', function(event) {
    if (confirm("Really reset quarter?")) {
        sendControl("RESET_QUARTER", 0);
    }
})

window.onkeydown = function(event) {
    if (event.keyCode === 32) {
        event.preventDefault();
        toggleClock();
    }
}
