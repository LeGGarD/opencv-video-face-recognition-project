////////////////////////////// WEBCAM WEBSOCKET //////////////////////////////


let webcam_place = document.getElementById("webcam");
let msg = document.getElementById("video");
let context = msg.getContext("2d");

function openSocket() {
    // number 1 in the end of the link below means that the websocket will be returning pure webcam stream
    var websocket = new WebSocket("ws://127.0.0.1:8000/ws_video/1");
    websocket.onmessage = (event) => {
        let image = new Image(msg.width, msg.height);
        const urlObject = URL.createObjectURL(event.data);
        image.src = urlObject;
        image.onload = (event) => {
            context.drawImage(image, 0, 0);
            URL.revokeObjectURL(urlObject);
            delete event
        };
        delete image
        delete event
    }
}

function openSocketFaceRecognition() {
    // number 2 in the end of the link below means that the websocket will be returning webcam stream with face recoognition
    var websocket = new WebSocket("ws://127.0.0.1:8000/ws_video/2");
    websocket.onmessage = (event) => {
        let image = new Image(msg.width, msg.height);
        const urlObject = URL.createObjectURL(event.data);
        image.src = urlObject;
        image.onload = (event) => {
            context.drawImage(image, 0, 0);
            URL.revokeObjectURL(urlObject);
            delete event
        };
        delete image
        delete event
    };
}


function showHide(id_1, id_2, flag) {
    var xmlHttp = new XMLHttpRequest();
    var button = document.getElementById('start');
    if (document.getElementById(id_1, id_2)){
        var obj = document.getElementById(id_1);
        var obj2 = document.getElementById(id_2);

        if (obj2.style.display == "none") {
            xmlHttp.open( "GET", "/video_start", false ); // false for synchronous request
            xmlHttp.send( null );
            if (flag === 1) {
                openSocket();
            }
            if (flag === 2) {
                openSocketFaceRecognition();
            }
            obj.style.display = "none"; // hide preview
            obj2.style.display = "inline-block"; // show video
            button.innerText = 'Зупинити';
            button.dataset.trigger = false;
            btn_photo.style.display = "inline-block";
        }
        else {
            xmlHttp.open( "GET", "/video_stop", false ); // false for synchronous request
            xmlHttp.send( null );
            obj.style.display = "block"; // show preview
            obj2.style.display = 'none'; // hide video
            button.innerText = 'Почати';
            button.dataset.trigger = true;
            btn_photo.style.display = "none";
        }
    }
    else alert("Элемент с id: " + element_id + " не найден!");
}

function showHideAddUser(id_1, id_2, id_3, flag) {
    var xmlHttp = new XMLHttpRequest();
    var button = document.getElementById('start');
    if (document.getElementById(id_1, id_2, id_3)){
        var obj = document.getElementById(id_1);
        var obj2 = document.getElementById(id_2);
        var obj3 = document.getElementById(id_3);

        if (obj2.style.display == "none") {
            xmlHttp.open( "GET", "/video_start", false ); // false for synchronous request
            xmlHttp.send( null );
            if (flag === 1) {
                openSocket();
            }
            if (flag === 2) {
                openSocketFaceRecognition();
            }
            obj.style.display = "none"; // hide preview
            obj2.style.display = "inline-block"; // show video
            obj3.style.display = "inline-block";
            button.innerText = 'Зупинити';
            button.dataset.trigger = false;
            btn_photo.style.display = "inline-block";
        }
        else {
            xmlHttp.open( "GET", "/video_stop", false ); // false for synchronous request
            xmlHttp.send( null );
            obj.style.display = "block"; // show preview
            obj2.style.display = 'none'; // hide video
            obj3.style.display = 'none';
            button.innerText = 'Почати';
            button.dataset.trigger = true;
            btn_photo.style.display = "none";
        }
    }
    else alert("Элемент с id: " + element_id + " не найден!");
}

////////////////////////////// MULTI FORM //////////////////////////////

const prevBtns = document.querySelectorAll(".btn-prev");
const nextBtns = document.querySelectorAll(".btn-next");
const progress = document.getElementById("progress");
const formSteps = document.querySelectorAll(".form-step");
console.log(formSteps)
const progressSteps = document.querySelectorAll(".progress-step");

let formStepsNum = 0;

function updateFormSteps() {
//  console.log(formSteps)
  formSteps.forEach((formStep) => {
    formStep.classList.contains("form-step-active") &&
      formStep.classList.remove("form-step-active");
  });

  formSteps[formStepsNum].classList.add("form-step-active");
}

function updateProgressbar() {
  progressSteps.forEach((progressStep, idx) => {
    if (idx < formStepsNum + 1) {
      progressStep.classList.add("progress-step-active");
    }
    else {
      progressStep.classList.remove("progress-step-active");
    }
  });

  const progressActive = document.querySelectorAll(".progress-step-active");

  progress.style.width =
    ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}

function buttonNext() {
    var name = document.getElementById("name").value;
    var address = document.getElementById("address").value;

    if (name != '' && address != '') {
        formStepsNum++;
        updateFormSteps();
        updateProgressbar();
        const labels = document.querySelectorAll('label');
        for (const label of labels) {
            label.classList.remove('red-text');
        }
    }
    else {
        document.getElementById('next-alert').style.display = 'inline-block'
        const labels = document.querySelectorAll('label');
        for (const label of labels) {
            label.classList.add('red-text');
        }
    }
}

function buttonPrevios() {
    formStepsNum--;
    updateFormSteps();
    updateProgressbar();

}

//////////////////////////////  FACE RECOGNITION   //////////////////////////////

let encodings = []
let taken_photos_span = document.getElementById("saved-photos");

let btn_photo = document.getElementById('photo')
let photo_text = document.getElementById('photo-text')

function takePhoto() {
    if (encodings.length < 5) {
        var xmlHttp = new XMLHttpRequest();
        var path = '/take_photo';
        xmlHttp.open( "GET", path, false ); // false for synchronous request
        xmlHttp.send( null );
        if (xmlHttp.responseText == '') {
            console.log('Webcam is turned off or face isn\'t found!')
        }
        else {
            encodings.push(xmlHttp.responseText)
            taken_photos_span.innerHTML = (parseInt(taken_photos_span.innerHTML) + 1).toString()
            console.log(encodings)
        }
        if (encodings.length == 5) {
            btn_photo.classList.remove('btn');
            btn_photo.classList.remove('btn-photo');
            btn_photo.classList.add('btn-disabled');
        }
    }
    else {
        console.log
    }
}

//////////////////////////////  CUSTOM FORM MANAGER   //////////////////////////////

const btn = document.querySelector('button');

function submitForm() {
    const XHR = new XMLHttpRequest();

    let urlEncodedData = "",
    urlEncodedDataPairs = [],
    name;

    if (encodings.length == 5 && name != '' && address != '') {
        var data = {'name': document.getElementById("name").value,
                  'address': document.getElementById("address").value,
                  'encodings': encodings}
        console.log(data)


        // Turn the data object into an array of URL-encoded key/value pairs.
        for ( name in data ) {
        urlEncodedDataPairs.push( encodeURIComponent( name ) + '=' + encodeURIComponent( data[name] ) );
        }

        console.log(urlEncodedDataPairs)

        // Combine the pairs into a single string and replace all %-encoded spaces to
        // the '+' character; matches the behaviour of browser form submissions.
        urlEncodedData = urlEncodedDataPairs.join( '&' ).replace( /%20/g, '+' );

        // Define what happens on successful data submission
//        XHR.addEventListener( 'load', function(event) {
//        alert( 'Yeah! Data sent and response loaded.' );
//        } );

        // Define what happens in case of error
        XHR.addEventListener( 'error', function(event) {
        alert( 'Oops! Something went wrong.' );
        } );

        // Set up our request
        XHR.open( 'POST', '/add_user/', false );

        // Add the required HTTP header for form data POST requests
        XHR.setRequestHeader( 'Content-Type', 'application/x-www-form-urlencoded' );

        // Finally, send our data.
        XHR.send( urlEncodedData );

        buttonNext();
    }
    else {
        console.log('Some inputs aren\'t filled or photos aren\'t taken')
        document.getElementById('submit-alert').style.display = 'inline-block'
    }
}
