// NOTE: Maybe there needs to be a listener to the onmessage function of the socket here (depends on frontend implementation)

var socket = null;
var isopen = false;
var resultJSON = null;
var isResultNew = false;

//Initializing the WebSocket
window.onload = function () {
    "use strict";

    // onclick handlers for buttons
    var btnSendText = document.getElementById("sendTextButton");
    btnSendText.onclick = function () {
        let el = document.getElementById("text_input");
        if (el) {
            let val = el.value;
            console.log("calling sendText() with:");
            console.log(val);
            sendText(val);
        }
    }

    var btnSendBinary = document.getElementById("sendBinaryButton");
    btnSendBinary.onclick = function () {
        console.log("calling sendBinary() with:");
        console.log(selected_file );
        sendBinary(selected_file);
    }

    // onchange handler for file dialog choice
    var selected_file = null;
    var fileInput = fileInput = document.getElementById("file_input");
    if (fileInput) {
        fileInput.onchange = function() {
            selected_file = fileInput.files[0];
        }
    } else {
        console.warn("Warning: file input not found");
    }

    //Currently the test and such the only port
    socket = new WebSocket("ws://127.0.0.1:9000");
    socket.binaryType = "arraybuffer";

    //Callback when the sockets recieves a message (should only be a result json here)
    socket.onmessage = function (result) {
        if (typeof result.data === "string") {
            console.log("Result text message received: " + result.data);
            resultJSON = result.data;
            isResultNew = true;
        } else {
            console.error("JS-Socket: Recieved response of wrong type");
        }
    };

    //Callback when the socket opens
    socket.onopen = function (e) {
        console.log("JS-Socket: Connected!");
        isopen = true;
    };

    //Callback when the socket closes
    socket.onclose = function (e) {
        console.log("JS-Socket: Connection closed.");
        socket = null;
        isopen = false;
    };
};

//function to call when sending text thru the socket
function sendText(jsonString) {
    "use strict";
    if (isopen) {
        if (typeof jsonString !== "string") {
            console.error("JS-Socket: Input has wrong type. String was expected");
        } else {
            socket.send(jsonString);
            console.log("JS-Socket: Text message sent.");
        }
    } else {
        console.log("JS-Socket: Connection not opened.");
    }
}

//function to call when sending an image(png) thru the socket
function sendBinary(file) {
    "use strict";
    if (isopen) {
        console.log("filename", file.name);
        console.log("file size", file.size);
       
        var reader = new FileReader();
        reader.onload = function () {
            // debugging
            console.log("result", reader.result);
            console.log("error", reader.error);

            // image transfer
            socket.send(reader.result);
            console.log("JS-Socket: Binary message sent.");
        }
        reader.readAsArrayBuffer(file);
        console.log("state", reader.readyState);
    } else {
        console.log("JS-Socket: Connection not opened.");
    }
}

//function to call when manually calling for a result
function getResult() {
    "use strict";
    if (resultJSON == null) {
        console.error("JS-Socket: Error - result not set");
        return null;
    }
    //If result is set then
    if (isResultNew) {
        return resultJSON;
    } else {
        console.warn("caution: returning old result");
        return resultJSON;
    }
}
