'use strict';
let submitClockButton = document.getElementById('submit_clock');
let clockInput = document.getElementById('clock_input');
let clock = document.getElementById('clock');
let toggleButton = document.getElementById('toggle_button');
let status = document.getElementById('status');
let resetQuarterButton = document.getElementById('reset_quarter');
let color = false;


var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/controller/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    console.log("message");
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

function updateStatusDisplay(data){

}

submitClockButton.addEventListener('click', function(event) {
    let clockValue = clockInput.value;
    clock.innerHTML = clockValue;

    sendControl("SET_CLOCK", clockValue);
});

toggleButton.addEventListener('click', function(event) {
    if (color) {
        status.style.backgroundColor = "#ff0000";
    }
    else {
        status.style.backgroundColor = "#00ff00";
    }
    color = !color;
    sendControl("TOGGLE_CLOCK", 0);
});

resetQuarterButton.addEventListener('click', function(event) {
    if (confirm("Really reset quarter?")) {
        sendControl("RESET_QUARTER", 0);
    }
})