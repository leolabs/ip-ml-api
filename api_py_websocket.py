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

class ApiWebsocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        sketch_conv = sketch_converter.SketchConverter()

        print(isBinary)
        # process sketch (as .png) from the frontend
        if isBinary:
            try:
                # convert payload to numpy array, so that the backend can work with it
                print(sketch_conv)
                print(sketch_conv.create_pil_image)

                image = sketch_conv.create_pil_image(payload)
                if image is None:
                    print("attempt to open unsupported file occured")

                numpy_array = sketch_conv.convert_to_numpy_array(image)
                if numpy_array is None:
                    print("an conversion error occured")
                    return

                # debugging
                print("received image")
                print(npy_data)

                # todo: call and wait for backend method/s

                # todo: construct .json out of results and labels

                # send .json to the frontend
                self.sendMessage("your sketch was identified as ...".encode('utf8'), isBinary=False)

            except Exception:
                return

        # process sketch (as .ndjson) from the frontend 
        else:
            try:
                decoded_payload = payload.decode('utf8')

                # todo: alter payload if necessary, so that the backend can work with it

                # todo: call and wait for backend method/s

                # todo: construct .json out of results and labels

                # send .json to the frontend
                self.sendMessage("your sketch was identified as ...".encode('utf8'), isBinary=False)

            except Exception:
                return

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

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

