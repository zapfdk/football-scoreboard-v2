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

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log(data["msg"]);
    if (data["msg"] === "UPDATE") {
        updateStatus(data["data"]);
    }
};

chatSocket.onopen = function (e) {
    let connStatus = document.getElementById("connection_status");
    connStatus.innerHTML = "connected";
    connStatus.style.color = "#00FF00";
};

chatSocket.onclose = function (e) {
    let connStatus = document.getElementById("connection_status");
    connStatus.innerHTML = "closed";
    connStatus.style.color = "#FF0000";
};

function updateStatus(data) {
    let elementPropDict = {
        "down": document.getElementById("current_down"),
        "quarter": document.getElementById("current_quarter"),
        "distance": document.getElementById("current_distance"),
        "score": [document.getElementById("score_home"), document.getElementById("score_guest")],
        "ball_on": document.getElementById("current_ballon"),
    };
    console.log(elementPropDict);
    console.log(data);
    for (let key in data) {
        if (data.hasOwnProperty(key) && key in elementPropDict) {
            if (key === "score" || key === "timeouts") {
                elementPropDict[key][0].innerHTML = data[key][0];
                elementPropDict[key][1].innerHTML = data[key][1];
            } else {
                elementPropDict[key].innerHTML = data[key];
            }
        }
    }
}

function sendControl(command, value) {
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

function setScore(teamId) {
    let teams = {0: "home", 1: "guest"};
    let score = Number(document.getElementById("score_"+teams[teamId]+"_input").value);
    console.log(teamId, score);
    sendControl('SET_SCORE', [score, teamId]);
    return false;
}

function setPossession() {

    sendControl('SET_POSESSION',);
}

function setTimeouts() {

    sendControl('SET_TIMEOUTS', []);
}

function changeGoallineBox(element) {
    let distIn = document.getElementById("distance_input");
    distIn.disabled = element.checked;
}
