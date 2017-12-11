
from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import pickle
import PIL.Image

class TestFrontendWebsocketProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def transfer_image():
            # open an image
            image = PIL.Image.open("input.png")

            # convert to bytes
            image_bytes = pickle.dumps(image)

            # transfer bytes
            self.sendMessage(image_bytes, isBinary=True)
            print("sent image")

            self.factory.loop.call_later(5, transfer_image)

        # start sending messages every 5 seconds ..
        transfer_image()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = TestFrontendWebsocketProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

