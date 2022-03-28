function openSocket() {
    let websocket = new WebSocket("ws://127.0.0.1:8000/ws_video");
    let msg = document.getElementById("video");
    websocket.onopen = (event) => {
        document.getElementById("status").innerHTML = "WebSocket connection is OPENED";
    };
    websocket.onmessage = (event) => {
        let context = msg.getContext("2d");
        let image = new Image();
        image.src = URL.createObjectURL(event.data);
        image.onload = (event) => {
            context.drawImage(image, 0, 0, msg.width, msg.height);
        };
    };
}

function closeSocket() {
    websocket.close();
}

function showHide(id_1, id_2) {
    var xmlHttp = new XMLHttpRequest();
    var button = document.getElementById('start');
    if (document.getElementById(id_1, id_2)){
        var obj = document.getElementById(id_1);
        var obj2 = document.getElementById(id_2);

        if (obj2.style.display == "none") {
            xmlHttp.open( "GET", "/video_start", false ); // false for synchronous request
            xmlHttp.send( null );
            openSocket();
            obj.style.display = "none"; // hide preview
            obj2.style.display = "inline-block"; // show video
            button.innerText = 'Stop';
            button.dataset.trigger = false;
        }
        else {
            xmlHttp.open( "GET", "/video_stop", false ); // false for synchronous request
            xmlHttp.send( null );
            obj.style.display = "block"; // show preview
            obj2.style.display = 'none'; // hide video
            button.innerText = 'Start';
            button.dataset.trigger = true;
        }
    }
    else alert("Элемент с id: " + element_id + " не найден!");
}


function parsePhoto() {
    var xmlHttp = new XMLHttpRequest();
    var user_id = getElementById('user_id');
    var path = '/add_user_step_2/recognize_face/' + user_id;
    xmlHttp.open( "GET", path, false ); // false for synchronous request
    xmlHttp.send( null );
}