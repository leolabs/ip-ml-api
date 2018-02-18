// NOTE: Maybe there needs to be a listener to the onmessage function of the socket here (depends on frontend implementation)

var socket = null;
var isopen = false;

//Initializing the WebSocket
window.onload = function () {
    "use strict";

    // onclick handlers for buttons
    var btnSendText = document.getElementById("sendTextButton");
    if (btnSendText) {
        btnSendText.onclick = function () {
            var el = document.getElementById("text_input");
            if (el) {
                var val = el.value;
                sendText(val);
            }
        }
    } else {
        console.warn("JS-Socket: send text button not found");
    }

    var btnSendBinary = document.getElementById("sendBinaryButton");
    if (btnSendBinary) {
        btnSendBinary.onclick = function () {
            sendBinary(selected_file);
        }
    } else {
        console.warn("JS-Socket: send binary button not found");
    }

    // onchange handler for file dialog choice
    var selected_file = null;
    var fileInput = fileInput = document.getElementById("file_input");
    if (fileInput) {
        fileInput.onchange = function () {
            selected_file = fileInput.files[0];
        }
    } else {
        console.warn("JS-Socket: file input not found");
    }

    //Currently the test and such the only port
    socket = new WebSocket("ws://127.0.0.1:9000");
    socket.binaryType = "arraybuffer";

    //Callback when the sockets recieves a message (should only be a result json here)
    socket.onmessage = function (result) {
        if (typeof result.data === "string") {
            console.log("JS-Socket: Message received | ", result.data);
            alert("JS-Socket: Message received\n\n" + result.data);
            return result.data;
        } else {
            console.error("JS-Socket: Recieved response of wrong type");
        }
    };

    //Callback when the socket opens
    socket.onopen = function (e) {
        console.log("JS-Socket: Connected");
        isopen = true;
    };

    //Callback when the socket closes
    socket.onclose = function (e) {
        console.log("JS-Socket: Connection closed");
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
            console.log("JS-Socket: Text message sent\n\n" + jsonString);
        }
    } else {
        console.log("JS-Socket: Connection not opened");
    }
}

//function to call when sending an image(png) thru the socket
function sendBinary(file) {
    "use strict";
    if (isopen) {
        // debugging
        console.log("Debug: File name | ", file.name);
        console.log("Debug: File size | ", file.size);

        var reader = new FileReader();
        reader.onload = function () {
            // debugging
            console.log("Debug: File reader result | ", reader.result);
            console.log("Debug: File reader error | ", reader.error);

            // image transfer
            socket.send(reader.result);
            console.log("JS-Socket: Binary message sent | ", file.name);
        }

        // read file into buffer
        reader.readAsArrayBuffer(file);
        console.log("Debug: File reader state | ", reader.readyState);
    } else {
        console.log("JS-Socket: Connection not opened");
    }
}
