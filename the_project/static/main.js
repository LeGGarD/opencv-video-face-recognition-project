//function getPngDimensions(string) {
//    console.log(string)
//    var base64 = btoa(string)
//    console.log(typeof base64)
//    console.log(base64)
//    let header = base64.slice(0, 50)
//    let uint8 = Uint8Array.from(atob(header), c => c.charCodeAt(0))
//    let dataView = new DataView(uint8.buffer, 0, 28)
//    console.log(dataView)
//    return {
//    "width": dataView.getInt32(16),
//    "height": dataView.getInt32(20)
//    }
//}

//function openSocket() {
//    let websocket = new WebSocket("ws://127.0.0.1:8000/ws_video");
//    let msg = document.getElementById("video");
//    var video_resolution = new Object();
//    websocket.onmessage = (event) => {
//
//        if (Object.keys(video_resolution).length < 2){
//            video_resolution = getPngDimensions(event.data);
//            console.log(video_resolution);
//        };
//        let context = msg.getContext("2d");
//        let image = new Image(video_resolution["width"], video_resolution["height"]);
//        image.src = URL.createObjectURL(event.data);
//        image.onload = (event) => {
//            context.drawImage(image, 0, 0);
//        };
//    };
//}

function openSocket() {
    let websocket = new WebSocket("ws://127.0.0.1:8000/ws_video");
    let msg = document.getElementById("video");
    websocket.onmessage = (event) => {
        let context = msg.getContext("2d");
        let image = new Image(msg.width, msg.height);
        image.src = URL.createObjectURL(event.data);
        image.style = "margin-left: auto; margin-right: auto;"
        image.onload = (event) => {
            context.drawImage(image, 0, 0);
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