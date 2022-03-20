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

function httpGet(theUrl)
    {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }

 function showHide(element_id, element_id_2) {
    var xmlHttp = new XMLHttpRequest();
    if (document.getElementById(element_id, element_id_2)){
        var obj = document.getElementById(element_id);
        var obj2 = document.getElementById(element_id_2);
        if (obj2.style.display == "none") {
            xmlHttp.open( "GET", "video_start", false ); // false for synchronous request
            xmlHttp.send( null );
            obj.style.display = "none"; // hide preview
            obj2.style.display = "block"; // show video

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

