'use strict';

Mousetrap.bindGlobal('d', function () {
    document.getElementById('down_1').focus();
});

Mousetrap.bindGlobal('q', function () {
    document.getElementById('quarter_1').focus();
});

Mousetrap.bindGlobal('t', function () {
    let distanceField = document.getElementById('distance_input');
    distanceField.focus();
    distanceField.value = "";
});

Mousetrap.bindGlobal('b', function () {
    let ballonField = document.getElementById('ballon_input');
    ballonField.focus();
    ballonField.value = "";
});

var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/controller/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    console.log(data);
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

function setDown() {
    let down = document.querySelector('input[name="down_radio"]:checked').value;
    sendControl('SET_DOWN', down);
    return false;
}

function setQuarter() {
    let quarter = document.querySelector('input[name="quarter_radio"]:checked').value;
    sendControl('SET_QUARTER', quarter);
    return false;
}

function setDistance() {
    let distance = document.getElementById('distance_input').value;
    sendControl('SET_DISTANCE', distance);
    return false;
}

function setBallon() {
    let ballon = document.getElementById('ballon_input').value;
    sendControl('SET_BALLON', ballon);
    return false;
}

function setScore() {

    sendControl('SET_SCORE', []);
    return false;
}

function setPossession() {
    
    sendControl('SET_POSESSION', );
}

function setTimeouts() {

    sendControl('SET_TIMEOUTS', []);
}

function changeGoallineBox(element) {
    let distIn = document.getElementById("distance_input");
    distIn.disabled = element.checked;
}
