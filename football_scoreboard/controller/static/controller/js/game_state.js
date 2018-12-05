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

function sendDown() {
    let down = document.querySelector('input[name="down_radio"]:checked').value;
    sendControl('SET_DOWN', down);
    return false;
}

function sendQuarter() {
    let quarter = document.querySelector('input[name="quarter_radio"]:checked').value;
    sendControl('SET_QUARTER', quarter);
    return false;
}

function sendDistance() {
    let distance = document.getElementById('distance_input').value;
    sendControl('SET_DISTANCE', distance);
    return false;
}

function sendBallon() {
    let ballon = document.getElementById('ballon_input').value;
    sendControl('SET_BALLON', ballon);
    return false;
}

