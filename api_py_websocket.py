###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


from SketchMe import SketchMe
import numpy as np
# todo: import backend
import sketch_converter
import json

#debugging
import PIL.Image

class ApiWebsocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("PY-Socket: Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("PY-Socket: WebSocket connection open")

    def onMessage(self, payload, isBinary):
        message_type = "binary" if (isBinary is not None and isBinary) else "text"
        print("PY-Socket: Received a {0} message".format(message_type))

        try:
            sketch_conv = sketch_converter.SketchConverter()

            # process sketch from the frontend (assuming that is in a format that is supported by PIL)
            if isBinary:

                # convert payload to numpy array, so that the backend can work with it
                image = sketch_conv.create_pil_image(payload)
                if image is None:
                    self.sendMessage("error: PIL can not operate on the given file".encode('utf8'), isBinary=False)
                    return

                numpy_array = sketch_conv.convert_to_numpy_array(image)
                if numpy_array is None:
                    self.sendMessage("error: PIL can not convert the given file".encode('utf8'), isBinary=False)
                    return

                backend_data = numpy_array

            # process sketch from the frontend (assuming that it is in .ndjson format)
            else:
                # interpret .ndjson data / text messages - this else block may be removed eventually (?)
                backend_data = payload.decode('utf8')

                # todo: alter payload if necessary, so that the backend can work with it
                # otherwise just pass the .ndjson data on to the backend in the next step

            # todo: call and wait for backend method/s
            self.sendMessage("status: waiting for the backend to process your request".encode('utf8'), isBinary=False)    
            Backend = SketchMe()
            Backend.Create_Model()

            # this is test code for the default images - may be removed eventually
            #test_image = np.load("DATA/ant.npy")
            #test_npy_data = test_image[-1]
            #print("test npy data")
            #print(test_npy_data)
            #print("prediction")
            #results = Backend.Predict(test_npy_data)
            #print(results)

            # this is where the received data is used
            results = Backend.Predict(backend_data)

            # construct json for categorized results
            with open('DATA/categories.txt') as f:
                self.categories = f.readlines()

            export_data = {}
            for i in range(0, len(self.categories)):
                category_key = self.categories[i].lower().replace('\n', '').replace(' ', '_').replace('-', '_')
                export_data[category_key] = "{0}".format(results[0][i])

            # send .json to the frontend
            payload = json.dumps(export_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf8')            
            self.sendMessage("status: your sketch was identified. results will arrive in the following message".encode('utf8'), isBinary=False)
            self.sendMessage(payload, isBinary=False)

            # debugging:
            print("[numpy array]\n")
            print(backend_data)
            print("[prediction results]\n")
            print(results)
            print("[export json]\n")
            print(payload)

        except Exception as e:
            print(e)
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

