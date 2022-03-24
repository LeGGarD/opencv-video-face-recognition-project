const button = document.getElementById('start');

button.addEventListener('click', () =>{
    if(button.dataset.trigger == 'false'){
        button.innerText = 'Start';
        button.dataset.trigger = true;
    }else{
        button.innerText = 'Stop';
        button.dataset.trigger = false;
    }
});

function openSocket() {
            websocket = new WebSocket("ws://127.0.0.1:8000/ws_video");
            let msg = document.getElementById("video");
            websocket.addEventListener('open', function (event) {
                document.getElementById("status").innerHTML = "WebSocket connection is OPENED";
            });
            websocket.addEventListener('message', function (event) {
                let context = msg.getContext("2d");
                let image = new Image();
                image.src = URL.createObjectURL(event.data);
                image.addEventListener("load", function (event) {
                    context.drawImage(image, 0, 0, msg.width, msg.height);
                });
            });
        }

function showHide(id_1, id_2) {
    var xmlHttp = new XMLHttpRequest();

    if (document.getElementById(id_1, id_2)){
        var obj = document.getElementById(id_1);
        var obj2 = document.getElementById(id_2);

        if (obj2.style.display == "none") {
            xmlHttp.open( "GET", "video_start", false ); // false for synchronous request
            xmlHttp.send( null );
            obj.style.display = "none"; // hide preview
            obj2.style.display = "inline-block"; // show video
        }
        else {
            xmlHttp.open( "GET", "video_stop", false ); // false for synchronous request
            xmlHttp.send( null );
            obj.style.display = "block"; // show preview
            obj2.style.display = 'none'; // hide video
        }
    }
    else alert("Элемент с id: " + element_id + " не найден!");
}