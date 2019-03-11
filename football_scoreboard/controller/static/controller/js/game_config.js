
var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/controller/');

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log(data);
};

chatSocket.onopen = function (e) {
};

chatSocket.onclose = function (e) {
};

function sendControl(command, value) {
    chatSocket.send(JSON.stringify({
        command: command,
        value: value
    }));
}

function setName(team){
    let name = document.getElementById(team+'_name_input').value;
    let teams = {"home": 0,
                "guest": 1}
    sendControl('SET_CONFIG_NAME', [name, teams[team]]);
    return false;
}