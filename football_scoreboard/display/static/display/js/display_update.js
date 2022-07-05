"use strict";

var FOOTBALL_CHAR = "&#127944";

//For leading zeros in minutes and seconds in clock
Number.prototype.pad = function(size) {
    var s = String(this);
    while (s.length < (size || 2)) {
        s = "0" + s;
    }
    return s;
};

function handle_gamestate_update(gamestate_data){
    Object.keys(gamestate_data).forEach(function (key){
        let value = gamestate_data[key];

        if (key === "gameclock"){
            let minutes = Math.floor(value/60);
            let seconds = value % 60;
            document.getElementsByClassName("minutes_clock")[0].innerHTML = minutes.toString().padStart(2, '0');
            document.getElementsByClassName("seconds_clock")[0].innerHTML = seconds.toString().padStart(2, '0');
        }

        else if (key === "gamestate"){
            Object.keys(gamestate_data[key]).forEach(function (gameStateKey){
                let gameStateValue = gamestate_data[key][gameStateKey];
                switch(gameStateKey){
                    case "score_home":
                        document.getElementsByClassName("score_home")[0].innerHTML = gameStateValue;
                    case "score_guest":
                        document.getElementsByClassName("score_guest")[0].innerHTML = gameStateValue;
                        break;
                    case "timeouts_home":
                        document.getElementsByClassName("timeouts_home")[0].innerHTML = gameStateValue;
                    case "timeouts_guest":
                        document.getElementsByClassName("timeouts_guest")[0].innerHTML = gameStateValue;
                        break;
                    case "quarter":
                        document.getElementsByClassName("quarter")[0].innerHTML = gameStateValue;
                        break;
                    case "distance":
                        let distance = gameStateValue;
                        if (distance > 0) {
                            document.getElementsByClassName("distance")[0].innerHTML = distance;
                        }
                        else if (distance === -1) {
                            document.getElementsByClassName("distance")[0].innerHTML = "Goal";
                        }
                        break;
                    case "ball_on":
                        document.getElementsByClassName("ball_on")[0].innerHTML = gameStateValue;
                        break;
                    case "down":
                        document.getElementsByClassName("down")[0].innerHTML = gameStateValue;
                        break;
                    case "possession":
                        let poss_classes = ["poss_home", "poss_guest"];
                        if (gameStateValue <= 1 & gameStateValue >= 0) {
                            document.getElementsByClassName(poss_classes[gameStateValue])[0].innerHTML = FOOTBALL_CHAR;
                            document.getElementsByClassName(poss_classes[1 - gameStateValue])[0].innerHTML = "";
                        }
                        if (gameStateValue === 2) {
                            document.getElementsByClassName(poss_classes[0])[0].innerHTML = "";
                            document.getElementsByClassName(poss_classes[1])[0].innerHTML = "";

                        }
                        break;
                }
            })
        }
        else if (key === "gameconfig"){
            let names = gamestate_data[key]["name"];
            document.getElementsByClassName("name_home")[0].innerHTML = names[0];
            document.getElementsByClassName("name_guest")[0].innerHTML = names[1];
        }
    });
}

function update_display() {
    fetch('/display/get_gamestatus')
        .then(function(response){
            return response.json();
        })
        .then(handle_gamestate_update)
        .catch(function(error) {
            console.error(error);
        });
}

setInterval(update_display, 500);
