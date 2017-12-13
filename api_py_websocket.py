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

# todo: import backend
import sketch_converter
import json

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
                backend_data = payload.decode('utf8')

                # todo: alter payload if necessary, so that the backend can work with it
                # otherwise just pass the .ndjson data on to the backend in the next step

            # debugging
            print("Debug: backend data before processing | {0}".format(backend_data))

            # todo: call and wait for backend method/s
            self.sendMessage("status: waiting for the backend to process your request".encode('utf8'), isBinary=False)    
            # backend methods, e.g. backend.perform(backend_data)

            # todo: construct .json out of results and labels

            # send .json to the frontend
            json_data = ['foo', {'bar': ('baz', None, 1.0, 2)}]
            payload = json.dumps(json_data, ensure_ascii=False).encode('utf8')
            self.sendMessage("status: your sketch was identified. results will arrive in the following message".encode('utf8'), isBinary=False)
            self.sendMessage(payload, isBinary=False)

        except Exception:
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

