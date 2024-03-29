'use strict';

var chatSocket;

function setupWebsocket(){
    chatSocket = new WebSocket('ws://' + window.location.host + '/ws/controller/');

    chatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        console.log(data["msg"]);
        if (data["msg"] === "UPDATE") {
            updateStatus(data["gamestate"]);
        }
        if ("transmissionStatus" in data){
            let lastTransmission = data["transmissionStatus"] + ": " + data["transmittedCommand"];
            document.getElementById("last_transmission").innerText = lastTransmission;
        }
        if ("gameconfig" in data){
            let gameconfig = data["gameconfig"];
            console.log(gameconfig);
            document.getElementById("name_home").innerText = gameconfig["name"][0];
            document.getElementById("name_guest").innerText = gameconfig["name"][1];
        }
    };

    chatSocket.onopen = function (e) {
        let connStatus = document.getElementById("connection_status");
        connStatus.innerHTML = "connected";
        connStatus.style.color = "#00FF00";
        document.getElementById("reconnect_button").style.display = "none";
    };

    chatSocket.onclose = function (e) {
        let connStatus = document.getElementById("connection_status");
        connStatus.innerHTML = "closed";
        connStatus.style.color = "#FF0000";
        document.getElementById("reconnect_button").style.display = "block";
    };
}

document.addEventListener("DOMContentLoaded", function(event) {
  setupWebsocket();
});

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



function updateStatus(data) {
    let elementPropDict = {
        "down": document.getElementById("current_down"),
        "quarter": document.getElementById("current_quarter"),
        "distance": document.getElementById("current_distance"),
        "score": [document.getElementById("score_home"), document.getElementById("score_guest")],
        "ball_on": document.getElementById("current_ballon"),
        "timeouts": [document.getElementById("current_timeouts_home"), document.getElementById("current_timeouts_guest")],
        "possession": document.getElementById("current_possession")
    };
    console.log(elementPropDict);
    console.log(data);
    for (let key in data) {
        if (data.hasOwnProperty(key) && key in elementPropDict) {
                console.log(key, data[key]);
            if (key === "score" || key === "timeouts") {
                elementPropDict[key][0].innerHTML = data[key][0];
                elementPropDict[key][1].innerHTML = data[key][1];
            } else {
                if (key === "distance" && data[key] === -1) {
                    elementPropDict[key].innerHTML = "to Goalline";
                } else {
                    elementPropDict[key].innerHTML = data[key];
                }
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
    if (document.getElementById("goalline_checkbox").checked) {
        distance = -1;
    }
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
    let score = Number(document.getElementById("score_" + teams[teamId] + "_input").value);
    console.log(teamId, score);
    sendControl('SET_SCORE', [score, teamId]);
    return false;
}

function setPossession() {
    let possession = document.querySelector('input[name="possession_radio"]:checked').value;
    sendControl('SET_POSSESSION', possession);
    return false;
}

function changeScore(teamId, value){
    sendControl('CHANGE_SCORE', [value, teamId]);
    return false;
}

function changeTimeouts(teamId, value){
    sendControl('CHANGE_TIMEOUTS', [value, teamId]);
    return false;
}

function setTimeouts(teamId) {
    let teams = {0: "home", 1: "guest"};
    let score = Number(document.getElementById("score_" + teams[teamId] + "_input").value);
    console.log(teamId, score);
    sendControl('SET_TIMEOUTS', [score, teamId]);
    return false;
}

function resetFirstDown(isGoalline) {
    if (confirm("Reset First Down?")) {
        let distance = 10;
        if (isGoalline) {
            distance = -1;
        }
        sendControl("SET_DOWN", 1);
        sendControl("SET_DISTANCE", distance);
    }
}

function resetHalf() {
    if (confirm("Reset Half?")) {
        sendControl("SET_DOWN", 1);
        sendControl("SET_DISTANCE", 10);
        sendControl("SET_BALLON", 35);
    }
}

function changeGoallineBox(element) {
    let distIn = document.getElementById("distance_input");
    distIn.disabled = element.checked;
}
