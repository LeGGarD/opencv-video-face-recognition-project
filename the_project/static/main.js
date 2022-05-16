////////////////////////////// WEBCAM WEBSOCKET //////////////////////////////

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
    } else {
      progressStep.classList.remove("progress-step-active");
    }
  });

  const progressActive = document.querySelectorAll(".progress-step-active");

  progress.style.width =
    ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}

function buttonNext() {
    formStepsNum++;
    updateFormSteps();
    updateProgressbar();
}

function buttonPrevios() {
    formStepsNum--;
    updateFormSteps();
    updateProgressbar();
}

//////////////////////////////  FACE RECOGNITION   //////////////////////////////

let encodings = []
let taken_photos_span = document.getElementById("saved-photos");

function takePhoto() {
    var xmlHttp = new XMLHttpRequest();
    var path = '/take_photo';
    xmlHttp.open( "GET", path, false ); // false for synchronous request
    xmlHttp.send( null );
    encodings.push(xmlHttp.responseText)
    taken_photos_span.innerHTML = (parseInt(taken_photos_span.innerHTML) + 1).toString()
    console.log(encodings)
}

//////////////////////////////  CUSTOM FORM MANAGER   //////////////////////////////

const btn = document.querySelector('button');

function sendData(data) {
  const XHR = new XMLHttpRequest();

  let urlEncodedData = "",
      urlEncodedDataPairs = [],
      name;1

  // Turn the data object into an array of URL-encoded key/value pairs.
  for ( name in data ) {
    urlEncodedDataPairs.push( encodeURIComponent( name ) + '=' + encodeURIComponent( data[name] ) );
  }

  // Combine the pairs into a single string and replace all %-encoded spaces to
  // the '+' character; matches the behaviour of browser form submissions.
  urlEncodedData = urlEncodedDataPairs.join( '&' ).replace( /%20/g, '+' );

  // Define what happens on successful data submission
  XHR.addEventListener( 'load', function(event) {
    alert( 'Yeah! Data sent and response loaded.' );
  } );

  // Define what happens in case of error
  XHR.addEventListener( 'error', function(event) {
    alert( 'Oops! Something went wrong.' );
  } );

  // Set up our request
  XHR.open( 'POST', 'https://example.com/cors.php' );

  // Add the required HTTP header for form data POST requests
  XHR.setRequestHeader( 'Content-Type', 'application/x-www-form-urlencoded' );

  // Finally, send our data.
  XHR.send( urlEncodedData );
}
