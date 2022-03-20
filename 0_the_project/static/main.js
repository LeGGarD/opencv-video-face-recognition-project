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

 function showHide(element_id, element_id_2) {
    if (document.getElementById(element_id, element_id_2)){
        var obj = document.getElementById(element_id);
        var obj2 = document.getElementById(element_id_2);
        if (obj2.style.display == "none") {
            obj.style.display = "none"; // hide preview
            // document.getElementById("video").src="{{ url_for('video_start') }}";
            obj2.style.display = "block"; // show video

        }
        else {
            obj.style.display = "block"; // show preview
            // document.getElementById("video").src="{{ url_for('video_stop') }}";
            obj2.style.display = 'none'; // hide video
        }
    }
    else alert("Элемент с id: " + element_id + " не найден!");
}

