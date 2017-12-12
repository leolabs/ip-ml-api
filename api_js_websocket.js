// NOTE: Maybe there needs to be a listener to the onmessage function of the socket here (depends on frontend implementation)

var socket = null;
var isopen = false;
var resultJSON = null;
var isResultNew = false;

//Initializing the WebSocket
window.onload = function () {
    "use strict";
    //Currently the test and such the only port
    socket = new WebSocket("ws://127.0.0.1:9000");
    socket.binaryType = "arraybuffer";

    //Callback when the socket opens
    socket.onopen = function () {
        console.log("JS-Socket: Connected!");
        isopen = true;
    };

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
        if (typeof jsonString !== "String") {
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
function sendBinary() {
    "use strict";
    if (isopen) {
        var buf = new ArrayBuffer(32);
        var arr = new Uint8Array(buf);
        for (i = 0; i < arr.length; ++i) {
            arr[i] = i;
        }
        socket.send(buf);
        console.log("JS-Socket: Binary message sent.");
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
