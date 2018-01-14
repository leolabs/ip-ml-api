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

import json
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

class ApiWebsocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("PY-Socket: Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("PY-Socket: WebSocket connection open")

    def onMessage(self, payload, isBinary):
        message_type = "binary" if (isBinary is not None and isBinary) else "text"
        print("PY-Socket: Received a {0} message".format(message_type))

        try:
            # consult backend to get image prediction results
            self.sendMessage("status: waiting for the backend to process your request".encode('utf8'), isBinary=False)    

            # construct json with categorized results
            export_data = {}
            export_data['lotus'] = "0.82310340232401253"
            export_data['cat'] = "0.42455013403243246"
            export_data['house'] = "0.03452320020413243"
            export_data['ship'] = "0.31435202320321325"
            export_data['ant'] = "0.13079054653644562"

            # send the prepared .json to the frontend
            payload = json.dumps(export_data, ensure_ascii=False, indent=4, separators=(',', ': ')).encode('utf8')            
            self.sendMessage(payload, isBinary=False)

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

