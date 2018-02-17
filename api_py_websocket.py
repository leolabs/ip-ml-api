from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import sys
sys.path.append('../ip-ml-tensorflow')
from SketchMe import SketchMe
import numpy as np
import sketch_converter
import json

class ApiWebsocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("PY-Socket: Client connecting: {0}".format(request.peer))
        self.backend = SketchMe()
        self.backend.Load_Model()

    def onOpen(self):
        print("PY-Socket: WebSocket connection open")

    def onMessage(self, message, isBinary):
        message_type = "binary" if (isBinary is not None and isBinary) else "text"
        print("PY-Socket: Received a {0} message".format(message_type))

        sketch = None

        # treat incoming messages that are in binary format as sketches in .png format
        if isBinary:
            try:
                sketch = sketch_converter.SketchConverter().convert_image(message)
            except sketch_converter.WrongImageFormatError:
                self.sendMessage("Please provide images in .png format".encode('utf8'), isBinary=False)
                return

            # pass the sketch on to the backend  
            prediction_results = self.backend.Predict(sketch)[0]

            # construct response for the frontend as .json with categorized prediction results
            export_data = {}
            for i in range(0, 5):
                result_index = prediction_results.argmax()
                category_key = self.backend.catNames[result_index].lower().replace('\n', '').replace(' ', '_').replace('-', '_')
                export_data[category_key] = "{0}".format(prediction_results[result_index])
                prediction_results[result_index] = 0.0 # set it to zero, so that the next iteration will return the second highest number, and so on...

            # send the prepared .json to the frontend
            response = json.dumps(export_data, ensure_ascii=False, indent=4, separators=(',', ': ')).encode('utf8')            
            self.sendMessage(response, isBinary=False)

        # treat incoming messages in text format as sketches in .ndjson format
        else:
            sketch = message.decode('utf8')
            self.sendMessage("Backend doesn't have support for .ndjson data! No results have been returned.".encode('utf8'), isBinary=False)    
            return

    def onClose(self, wasClean, code, reason):
        print("PY-Socket: WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = ApiWebsocketProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()

